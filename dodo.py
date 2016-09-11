import glob
import os
import re
import shutil
import tempfile
from urllib import request

from doit.action import CmdAction
from doit.exceptions import TaskFailed
from doit import get_var

config = {
    'pandoc': get_var('pandoc', 'pandoc'),
    'pylupdate5': get_var('pylupdate5', 'pylupdate5'),
    'lrelease': get_var('lrelease', 'lrelease'),
    'pyrcc5': get_var('pyrcc5', 'pyrcc5'),
    'pyuic5': get_var('pyuic5', 'pyuic5'),
    'pip': get_var('pip', 'pip'),
    'pyenv': get_var('pyenv', 'pyenv')
}

DOIT_CONFIG = {
    'default_tasks': [
        'install_dependencies',
        'convert_md',
        'download_icons',
        'download_qtbase_ts',
        'update_ts',
        'generate_qm'
    ]
}


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
    def do_nothing():
        pass

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

    def check_pandoc():
        if not shutil.which(config['pandoc']):
            return TaskFailed("'{}' not found.".format(config['pandoc']))

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
        yield {
            'name': file,
            'file_dep': [file],
            'actions': [(check_pandoc), '{} -s -S {} -o {}'.format(config['pandoc'], file, rst_file_path)],
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

    def check_lxml():
        try:
            import lxml
        except ImportError:
            return TaskFailed("'lxml' package not found. Please install it. (pip install lxml)")

    def download_icon(icon):
        from lxml import html
        if not os.path.isfile(get_icon_path(icon)):
            download_page_url = "https://commons.wikimedia.org/wiki/File:Gnome-{}.svg".format(icon)
            with request.urlopen(download_page_url) as download_page_response:
                download_page_content = download_page_response.read()
                download_page_tree = html.fromstring(download_page_content)
                icon_urls = download_page_tree.xpath('//div[@class="fullImageLink"]/a/@href')
                if len(icon_urls) > 0:
                    with request.urlopen(icon_urls[0]) as icon_response:
                        icon_content = icon_response.read()
                        os.makedirs(icons_dir, exist_ok=True)
                        with open(os.path.join(icons_dir, icon + '.svg'), '+wb') as f:
                            f.write(icon_content)

    def get_icon_path(icon):
        return os.path.join(icons_dir, '{}.svg'.format(icon))

    def check_outdated(icon):
        if not os.path.isfile(get_icon_path(icon)):
            return False
        return True

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
            'actions': [(check_lxml), (download_icon, [icon])],
            'targets': [icon_path],
            'uptodate': [(check_outdated, [icon], {})]
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
        language_qtbase_ts_path = get_language_qtbase_ts_path(language)
        if not os.path.isfile(language_qtbase_ts_path):
            url = "http://l10n-files.qt.io/l10n-files/qt5-old/qtbase_{}.ts".format(language)
            with request.urlopen(url) as response:
                content = response.read()
                with open(language_qtbase_ts_path, "wb+") as f:
                    f.write(content)
                    f.close()

    def get_language_qtbase_ts_path(language):
        return os.path.join(locale_dir, 'qtbase_{}.ts'.format(language))

    def check_outdated(language):
        if not os.path.isfile(get_language_qtbase_ts_path(language)):
            return False
        return True

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
            'actions': [(download_qtbase_ts, [language])],
            'targets': [language_qtbase_ts_path],
            'uptodate': [(check_outdated, [language])]
        }

def task_update_ts():
    genial_pro_path = "genial.pro"

    def check_pylupdate5():
        if not shutil.which(config['pylupdate5']):
            return TaskFailed("'{}' not found.".format(config['pylupdate5']))

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
        'file_dep': sources + forms,
        'actions': [check_pylupdate5, CmdAction(generate_pylupdate5_cmd, [pro_file_content])],
        'targets': [genial_pro_path] + translations,
        'verbosity': 2
    }


def task_generate_qm():

    def check_lrelease():
        if not shutil.which(config['lrelease']):
            return TaskFailed("'{}' not found.".format(config['lrelease']))

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

        yield {
            'name': 'genial_' + language,
            'actions': [(check_lrelease), CmdAction('{} {} -qm {}'.format(config['lrelease'], genial_ts_file, genial_qm_file))],
            'file_dep': [genial_ts_file],
            'targets': [genial_qm_file],
            'task_dep': ['update_ts']
        }

        yield {
            'name': 'qtbase_' + language,
            'actions': [(check_lrelease), CmdAction('{} {} -qm {}'.format(config['lrelease'], qtbase_ts_file, qtbase_qm_file))],
            'file_dep': [qtbase_ts_file],
            'targets': [qtbase_qm_file],
            'task_dep': ['update_ts']
        }