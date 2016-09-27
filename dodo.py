import datetime
import glob
import hashlib
import importlib
import math
import multiprocessing
import os
import platform
import re
import shlex
import shutil
import subprocess
import tarfile
import time
import zipfile

from urllib.parse import urlparse

from doit.action import CmdAction
from doit.exceptions import TaskFailed, TaskError
from doit.tools import run_once
from doit import get_var

''' ============== '''
''' === CONFIG === '''
''' ============== '''

default = {
    'pandoc': 'pandoc',
    'pylupdate5': 'pylupdate5',
    'lrelease': 'lrelease',
    'pyrcc5': 'pyrcc5',
    'pyuic5': 'pyuic5',
    'pip': 'pip',
    'pyenv': 'pyenv',
    'make': 'make',
    'gist': 'gist',
    'hg': 'hg',
    'python': 'python',
    'cx_freeze_url': 'https://bitbucket.org/anthony_tuininga/cx_freeze',
    'cx_freeze_dir': 'cx_freeze'
}

config = {
    'pandoc': get_var('pandoc', default['pandoc']),
    'pylupdate5': get_var('pylupdate5', default['pylupdate5']),
    'lrelease': get_var('lrelease', default['lrelease']),
    'pyrcc5': get_var('pyrcc5', default['pyrcc5']),
    'pyuic5': get_var('pyuic5', default['pyuic5']),
    'pip': get_var('pip', default['pip']),
    'pyenv': get_var('pyenv', default['pyenv']),
    'gist': get_var('gist', default['gist']),
    'hg': get_var('hg', default['hg']),
    'python': get_var('python', default['python']),
    'cx_freeze_url': get_var('cx_freeze_url', default['cx_freeze_url']),
    'cx_freeze_dir': get_var('cx_freeze_dir', default['cx_freeze_dir'])
}


''' =================== '''
''' === DOIT CONFIG === '''
''' =================== '''


DOIT_CONFIG = {
    'default_tasks': [
        'setup_cx_freeze_repository',
        'install_cx_freeze',
        'install_dependencies',
        'convert_md',
        'download_icons',
        'download_qtbase_ts',
        'update_ts',
        'generate_qm',
        'generate_locale',
        'generate_icons',
        'generate_plugins',
        'compile_qrc',
        'compile_ui'
    ]
}


common_params = {
    'force': {
        'name': 'force',
        'short': 'f',
        'long': 'force',
        'type': bool,
        'default': False
    }
}


''' ============== '''
''' === CHECKS === '''
''' ============== '''


def is_continuous_integration():
    return os.environ.get('CONTINUOUS_INTEGRATION') is not None


def check_cmd(*commands):
    for command in commands:
        if not shutil.which(command):
            return TaskFailed("'{}' not found.".format(command))
    return True


def check_module(*modules):
    for module in modules:
        try:
            importlib.import_module(module)
        except ImportError:
            return TaskFailed("'{}' module not found.".format(module))
    return True


def check_is_file(path):
    return os.path.isfile(path)


def check_is_not_file(path):
    return not check_is_file(path)


def check_is_dir(path):
    return os.path.isdir(path)


def check_is_not_dir(path):
    return not check_is_dir(path)


''' ================= '''
''' === UTILITIES === '''
''' ================= '''


def update_gist(file):
    if is_continuous_integration() and check_cmd('gist') is not TaskFailed:
        gist_id = 'a9ada04ad9ee0b1920994b7a55f22774'

        command = shlex.split('gist -u {} {}'.format(gist_id, file))

        p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = p.communicate()
        if p.poll() > 0:
            return TaskError("Command '{}' failed.\n{}".format(" ".join(command), out))


def download_file(url, target_path):
    import requests

    r = requests.get(url, stream=True)
    start = datetime.datetime.now()
    moment_ago = start
    downloaded_size = 0
    print("Downloading {}:".format(url))
    with open(target_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
            now = datetime.datetime.now()
            if moment_ago + datetime.timedelta(seconds=1) < now:
                print(
                    "\rDownloaded {:2d}%".format(
                        downloaded_size / int(r.headers['content-length'])
                    ),
                    end=""
                )
                moment_ago = now
    print("")
    print("Finished downloading '{}'.".format(url))


def extract_zip(zip_path, extract_path):
    print("Extracting '{}' to '{}'".format(zip_path, extract_path))
    print("Currently here: {}".format(os.getcwd()))
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(path=extract_path)


def extract_tar(tar_path, extract_path):
    print("Extracting '{}' to '{}'".format(tar_path, extract_path))
    print("Currently here: {}".format(os.getcwd()))

    if os.path.splitext(tar_path)[1] == '.xz':
        mode = 'r:xz'
    else:
        mode = 'r:*'

    with tarfile.open(tar_path, mode=mode) as tf:
        tf.extractall(path=extract_path)


def cmd_with_animation(cmd="", path=".", log_file=None):
    current_path = os.getcwd()
    log_file_path = os.path.join(path, log_file)

    p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    subprocess_wait_animation(p)
    out, err = p.communicate()

    if not log_file:
        print(out.strip())
    else:
        with open(log_file_path, 'w') as f:
            f.write(out)
    if p.poll() > 0:
        return TaskError("Command '{}' failed.\n{}".format(" ".join(cmd), err))


def subprocess_wait_animation(p):
    anim_frames = ['▀', '▐', '▄', '▌']
    if p.poll() is None:
        counter = 0
        start_time = datetime.datetime.now()
        moment_ago = start_time
        while p.poll() is None:
            now = datetime.datetime.now()
            if moment_ago + datetime.timedelta(seconds=1) > now:
                print('\r{}'.format(anim_frames[counter]), end="")
                counter += 1
                counter %= len(anim_frames)
                moment_ago = now
            time.sleep(0.25)
        print("\r \r", end="")


def lazy_read(file_object, chunks=1024):
    # http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    while True:
        data = file_object.read(chunks)
        if not data:
            break
        yield data


def check_sum(path, type='md5', digest=''):
    if not os.path.isfile(path):
        return TaskFailed("'{}' is not a file. Cannot checksum.".format(path))

    if type == 'md5':
        m = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in lazy_read(f):
                m.update(chunk)
        md5_sum = m.hexdigest()

        if digest == md5_sum:
            print("'{}' ({}) matches the md5sum. ".format(path, digest))
            return True
        else:
            return TaskFailed("'{}' ({}) do not match the md5sum.".format(path, digest))
    else:
        return TaskFailed("'{}' is not a suppported sum type.".format(type))


def do_nothing():
    pass


''' ============= '''
''' === TASKS === '''
''' ============= '''

''' --- DEFAULT TASKS --- '''


def task_install_dependencies():
    return {
        'file_dep': ['doit_requirements.txt'],
        'actions': [
            CmdAction('{} install -r doit_requirements.txt'.format(config['pip']))
        ],
        'verbosity': 2,
        'setup': ['rehash_pyenv']
    }


def task_rehash_pyenv():
    if not shutil.which(config['pyenv']):
        return {
            'actions': [do_nothing]
        }
    else:
        return {
            'actions': [do_nothing],
            'teardown': [CmdAction('{} rehash'.format(config['pyenv']))]
        }


def task_convert_md():
    files = glob.glob("**.md", recursive=True)

    yield {
        'basename': 'convert_md',
        'name': None,
        'watch': ['.'],
        'doc': 'Converts project .md files to .rst'
    }

    for file in files:
        file_name = os.path.splitext(os.path.basename(file))
        dir_name = os.path.dirname(file)
        rst_file_path = os.path.join(dir_name, file_name[0] + ".rst")
        pandoc = config['pandoc']
        yield {
            'name': file,
            'file_dep': [file],
            'actions': [(check_cmd, [pandoc]), '{} -s -S {} -o {}'.format(pandoc, file, rst_file_path)],
            'targets': [rst_file_path]
        }


def task_download_icons():
    icons = [
        'document-new',
        'document-open',
        'document-save',
        'document-save-as',
        'edit-undo',
        'edit-redo',
        'edit-cut',
        'edit-copy',
        'edit-paste',
        'document-properties',
        'document-print',
        'document-print-preview',
        'application-exit',
        'window-close',
        'list-add',
        'list-remove',
        'go-up',
        'go-down'
    ]
    icons_dir = "genial/resources/icons"

    def download_icon(icon):
        import requests
        from lxml import html

        if not os.path.isfile(get_icon_path(icon)):
            download_page_url = "https://commons.wikimedia.org/wiki/File:Gnome-{}.svg".format(icon)
            download_page_response = requests.get(download_page_url)
            download_page_tree = html.fromstring(download_page_response.text)
            icon_urls = download_page_tree.xpath('//div[@class="fullImageLink"]/a/@href')
            if len(icon_urls) > 0:
                icon_response = requests.get(icon_urls[0])
                os.makedirs(icons_dir, exist_ok=True)
                with open(os.path.join(icons_dir, icon + '.svg'), '+wb') as f:
                    f.write(icon_response.content)

    def get_icon_path(icon):
        return os.path.join(icons_dir, '{}.svg'.format(icon))

    yield {
        'basename': 'download_icons',
        'name': None,
        'watch': [icons_dir],
        'doc': 'Download icons from GNOME Desktop icons project.'
    }

    for icon in icons:
        icon_path = get_icon_path(icon)
        yield {
            'name': icon,
            'actions': [(check_module, ['requests', 'lxml']), (download_icon, [icon])],
            'targets': [icon_path],
            'uptodate': [(check_is_file, [get_icon_path(icon)])]
        }


def task_download_qtbase_ts():
    locale_dir = "genial/resources/locale"
    languages = []
    for file in os.listdir(locale_dir):
        if file.endswith(".ts"):
            match = re.match(r'genial_(.*)\.ts', file)
            if match is not None:
                languages.append(match.group(1))

    def download_qtbase_ts(language):
        import requests

        language_qtbase_ts_path = get_language_qtbase_ts_path(language)
        if not os.path.isfile(language_qtbase_ts_path):
            url = "http://l10n-files.qt.io/l10n-files/qt5-old/qtbase_{}.ts".format(language)
            response = requests.get(url)
            with open(language_qtbase_ts_path, "wb+") as f:
                f.write(response.content)

    def get_language_qtbase_ts_path(language):
        return os.path.join(locale_dir, 'qtbase_{}.ts'.format(language))

    yield {
        'basename': 'download_qtbase_ts',
        'name': None,
        'watch': [locale_dir],
        'doc': 'Download qtbase file for each supported language other than English.'
    }

    for language in languages:
        language_qtbase_ts_path = get_language_qtbase_ts_path(language)
        yield {
            'name': language,
            'actions': [(check_module, ['requests']), (download_qtbase_ts, [language])],
            'targets': [language_qtbase_ts_path],
            'uptodate': [(check_is_file, [get_language_qtbase_ts_path(language)])]
        }


def task_update_ts():
    genial_pro_path = "genial.pro"

    def generate_pylupdate5_cmd():
        with open(genial_pro_path, 'w+') as pro_file:
            pro_file.write(pro_file_content)
            pro_file.close()
        return "{} -verbose -translate-function '_translate' {}".format(
            config['pylupdate5'], genial_pro_path
        )

    src_dir = "genial"
    sources = []
    forms = []
    translations = []

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                if not (re.match(r'ui_(.*)\.py', file) or re.match(r'__init__\.py', file)):
                    sources.append(os.path.join(root, file))
            elif file.endswith(".ui"):
                forms.append(os.path.join(root, file))
            elif file.endswith(".ts"):
                if not re.match(r'qtbase_(.*)\.ts', file):
                    translations.append(os.path.join(root, file))

    pro_file_content = "SOURCES = " + " \\\n".join(sources) + "\n\n"
    pro_file_content += "FORMS = " + " \\\n".join(forms) + "\n\n"
    pro_file_content += "TRANSLATIONS = " + " \\\n".join(translations)

    return {
        'task_dep': ['download_qtbase_ts'],
        'actions': [(check_cmd, ['pylupdate5']), CmdAction(generate_pylupdate5_cmd, [pro_file_content])],
        'targets': [genial_pro_path] + translations,
        'verbosity': 2
    }


def task_generate_qm():
    locale_dir = "genial/resources/locale"
    languages = []

    for file in os.listdir(locale_dir):
        if file.endswith(".ts"):
            match = re.match(r'genial_(.*)\.ts', file)
            if match is not None:
                languages.append(match.group(1))

    yield {
        'basename': 'generate_qm',
        'name': None,
        'watch': [locale_dir],
        'doc': 'Generate .qm files from .ts files',
        'task_dep': ['update_ts']
    }

    for language in languages:
        genial_ts_file = os.path.join(locale_dir, "genial_{}.ts".format(language))
        genial_qm_file = os.path.join(locale_dir, "genial_{}.qm".format(language))
        qtbase_ts_file = os.path.join(locale_dir, "qtbase_{}.ts".format(language))
        qtbase_qm_file = os.path.join(locale_dir, "qtbase_{}.qm".format(language))

        lrelease = config['lrelease']

        yield {
            'name': 'genial_' + language,
            'actions': [
                (check_cmd, [lrelease]),
                CmdAction('{} {} -qm {}'.format(lrelease, genial_ts_file, genial_qm_file))
            ],
            'file_dep': [genial_ts_file],
            'targets': [genial_qm_file],
            'task_dep': ['update_ts']
        }

        yield {
            'name': 'qtbase_' + language,
            'actions': [
                (check_cmd, [lrelease]),
                CmdAction('{} {} -qm {}'.format(config['lrelease'], qtbase_ts_file, qtbase_qm_file))
            ],
            'file_dep': [qtbase_ts_file],
            'targets': [qtbase_qm_file],
            'task_dep': ['update_ts']
        }


def task_generate_locale():
    def create_rcc():
        if files_found:
            with open(target, 'w+') as f:
                f.write(qrc_content)

    resources_dir = "genial/resources"
    locale_dir = os.path.join(resources_dir, "locale")
    target = os.path.join(resources_dir, 'locale.qrc')
    qrc_content = "<RCC>"
    qrc_content += '\n  <qresource prefix="/locale">'
    files_found = []
    os.makedirs(locale_dir, exist_ok=True)
    for file in os.listdir(locale_dir):
        if file.endswith(".qm"):
            files_found.append(os.path.join(locale_dir, file))
            qrc_content += "\n    <file alias='{0}'>locale/{0}</file>".format(file)
    qrc_content += "\n  </qresource>"
    qrc_content += "\n</RCC>\n"

    return {
        'task_dep': ['generate_qm'],
        'file_dep': files_found,
        'actions': [create_rcc],
        'targets': [target],
        'verbosity': 2
    }


def task_generate_icons():
    def create_rcc():
        if files_found:
            with open(target, 'w+') as f:
                f.write(qrc_content)

    resources_dir = "genial/resources"
    icons_dir = os.path.join(resources_dir, "icons")
    target = os.path.join(resources_dir, 'icons.qrc')
    qrc_content = "<RCC>"
    qrc_content += '\n  <qresource prefix="/icons">'
    files_found = []
    os.makedirs(icons_dir, exist_ok=True)
    for file in os.listdir(icons_dir):
        if file.endswith(".svg"):
            files_found.append(os.path.join(icons_dir, file))
            qrc_content += "\n    <file alias='{0}'>icons/{0}</file>".format(file)
    qrc_content += "\n  </qresource>"
    qrc_content += "\n</RCC>\n"

    return {
        'task_dep': ['download_icons'],
        'file_dep': files_found,
        'actions': [create_rcc],
        'targets': [target],
        'verbosity': 2
    }


def task_generate_plugins():
    def create_rcc():
        if files_found:
            with open(target, 'w+') as f:
                f.write(qrc_content)

    resources_dir = "genial/resources"
    plugins_dir = os.path.join(resources_dir, "plugins")
    target = os.path.join(resources_dir, 'plugins.qrc')
    qrc_content = "<RCC>"
    qrc_content += '\n  <qresource prefix="/icons">'
    files_found = []
    os.makedirs(plugins_dir, exist_ok=True)

    current_dir = os.getcwd()
    os.chdir(resources_dir)
    for root, dirs, files in os.walk("plugins"):
        for file in files:
            if file.endswith(".genial-plugin") or file.endswith(".py"):
                if platform.system() != "Windows":
                    plugin_dir = root.replace("plugins/", "")
                else:
                    plugin_dir = root.replace("plugins\\", "")
                files_found.append(os.path.join(plugins_dir, plugin_dir, file))
                qrc_content += "\n    <file alias='{}'>{}</file>".format(
                    os.path.join(plugin_dir, file),
                    os.path.join(root, file)
                )
    os.chdir(current_dir)

    qrc_content += "\n  </qresource>"
    qrc_content += "\n</RCC>\n"

    return {
        'file_dep': files_found,
        'actions': [create_rcc],
        'targets': [target],
        'verbosity': 2
    }


def task_compile_qrc():
    resources_dir = "genial/resources"

    yield {
        'basename': 'compile_qrc',
        'name': None,
        'watch': [resources_dir],
        'doc': 'Compiles *.qrc files to *_rc.py',
        'task_dep': ['generate_locale', 'generate_icons', 'generate_plugins']
    }

    for file in os.listdir(resources_dir):
        if file.endswith(".qrc"):
            output_file = re.sub(r'(.*)\.qrc', r'\1_rc.py', file)
            file_full_path = os.path.join(resources_dir, file)
            output_file_full_path = os.path.join(resources_dir, output_file)

            pyrcc5 = config['pyrcc5']

            yield {
                'name': file,
                'actions': [(check_cmd, [pyrcc5]),
                            CmdAction('{} {} -o {}'.format(pyrcc5, file_full_path, output_file_full_path))],
                'file_dep': [file_full_path],
                'targets': [output_file_full_path]
            }


def task_compile_ui():
    ui_dir = "genial/ui"
    gen_dir = "genial/views/gen"

    yield {
        'basename': 'compile_ui',
        'name': None,
        'watch': [ui_dir],
        'doc': 'Compiles *.ui files to ui_*.py'
    }

    for file in os.listdir(ui_dir):
        if file.endswith(".ui"):
            output_file = re.sub(r'(.*)\.ui', r'ui_\1.py', file)
            file_full_path = os.path.join(ui_dir, file)
            output_file_full_path = os.path.join(gen_dir, output_file)

            pyuic5 = config['pyuic5']

            yield {
                'name': file,
                'actions': [
                    (check_cmd, [pyuic5]),
                    CmdAction(
                        '{} --import-from=genial.resources {} -o {}'.format(
                            pyuic5, file_full_path, output_file_full_path
                        )
                    )
                ],
                'file_dep': [file_full_path],
                'targets': [output_file_full_path]
            }


def task_setup_cx_freeze_repository():
    _clone_cmd = shlex.split("{} clone {}".format(config['hg'], config['cx_freeze_url']))

    def make_dirs(dir_name, task):
        if task.options['force']:
            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)

    def check_uptodate(task):
        if task.options and task.options.get('force'):
            return False
        else:
            return check_is_dir(config['cx_freeze_dir'])

    return {
        'actions': [
            (check_cmd, [config['hg']]),
            (make_dirs, [config['cx_freeze_dir']]),
            _clone_cmd
        ],
        'uptodate': [check_uptodate],
        'params': [common_params['force']]
    }


def task_install_cx_freeze():
    _cx_freeze_dir = config['cx_freeze_dir']
    _python_bin = config['python']
    _build_install_cmd = shlex.split(
        "(cd {0} && {1} setup.py build && {1} setup.py install)".format(_cx_freeze_dir, _python_bin)
    )

    def check_uptodate(task):
        if task.options and task.options.get('force'):
            return False
        else:
            return check_module("cx_Freeze") is True

    return {
        'task_dep': ['setup_cx_freeze_repository'],
        'actions': [_build_install_cmd],
        'uptodate': [check_uptodate],
        'params': [common_params['force']]
    }

