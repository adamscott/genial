import glob
import os
import platform
import re
import shutil

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
    'pyenv': get_var('pyenv', 'pyenv'),
    'pyqtdeploycli': get_var('pyqtdeploycli', 'pyqtdeploycli')
}

DOIT_CONFIG = {
    'default_tasks': [
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


''' ============== '''
''' === CHECKS === '''
''' ============== '''


def check_lxml():
    try:
        import lxml
    except ImportError:
        return TaskFailed("'lxml' package not found. Please install it. (pip install lxml)")


def check_requests():
    try:
        import requests
    except ImportError:
        return TaskFailed("'requests' package not found. Please install it. (pip install requests)")


def check_pandoc():
    if not shutil.which(config['pandoc']):
        return TaskFailed("'{}' not found.".format(config['pandoc']))


def check_pylupdate5():
    if not shutil.which(config['pylupdate5']):
        return TaskFailed("'{}' not found.".format(config['pylupdate5']))


def check_lrelease():
    if not shutil.which(config['lrelease']):
        return TaskFailed("'{}' not found.".format(config['lrelease']))


def check_pyrcc5():
    if not shutil.which(config['pyrcc5']):
        return TaskFailed("'{}' not found.".format(config['pyrcc5']))


def check_pyuic5():
    if not shutil.which(config['pyuic5']):
        return TaskFailed("'{}' not found.".format(config['pyuic5']))


def check_pyqtdeploycli():
    if not shutil.which(config['pyqtdeploycli']):
        return TaskFailed("'{}' not found.".format(config['pyqtdeploycli']))


def do_nothing():
    pass


''' ============= '''
''' === TASKS === '''
''' ============= '''

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
            'actions': [(check_requests), (check_lxml), (download_icon, [icon])],
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
        import requests

        language_qtbase_ts_path = get_language_qtbase_ts_path(language)
        if not os.path.isfile(language_qtbase_ts_path):
            url = "http://l10n-files.qt.io/l10n-files/qt5-old/qtbase_{}.ts".format(language)
            response = requests.get(url)
            with open(language_qtbase_ts_path, "wb+") as f:
                f.write(response.content)

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
            'actions': [check_requests, (download_qtbase_ts, [language])],
            'targets': [language_qtbase_ts_path],
            'uptodate': [(check_outdated, [language])]
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
        'actions': [check_pylupdate5, CmdAction(generate_pylupdate5_cmd, [pro_file_content])],
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
            qrc_content += "\n    <file alias='{}'>locale/{}</file>".format(file, file)
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
            qrc_content += "\n    <file alias='{}'>icons/{}</file>".format(file, file)
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

            yield {
                'name': file,
                'actions': [(check_pyrcc5),
                            CmdAction('{} {} -o {}'.format(config['pyrcc5'], file_full_path, output_file_full_path))],
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

            yield {
                'name': file,
                'actions': [(check_pyuic5),
                            CmdAction('{} --import-from=genial.resources {} -o {}'.format(config['pyuic5'], file_full_path, output_file_full_path))],
                'file_dep': [file_full_path],
                'targets': [output_file_full_path]
            }


def task_create_pdy():
    target_pdy = 'genial.pdy'

    default_python_major = 3
    default_python_minor = 5
    default_python_patch = 2
    default_source_dir = os.path.join(
        os.path.expanduser('~'),
        '.pyenv/sources/{}.{}.{}/Python'.format(
            default_python_major, default_python_minor, default_python_patch
        )
    )
    default_include_dir = os.path.join(
        os.path.expanduser('~'),
        '.pyenv/versions/{}.{}.{}/include/python{}.{}m'.format(
            default_python_major, default_python_minor, default_python_patch,
            default_python_major, default_python_minor
        )
    )
    default_python_library = os.path.join(
        os.path.expanduser('~'),
        '.pyenv/versions/{}.{}.{}/lib/libpython{}.{}m.a'.format(
            default_python_major, default_python_minor, default_python_patch,
            default_python_major, default_python_minor
        )
    )
    default_standard_library_dir = os.path.join(
        os.path.expanduser('~'),
        '.pyenv/versions/{}.{}.{}/lib/python{}.{}'.format(
            default_python_major, default_python_minor, default_python_patch,
            default_python_major, default_python_minor
        )
    )

    exclusion_list = [
        re.compile('.*\.pyc$'), re.compile('.*\.pyd$'), re.compile('.*\.pyo$'),
        re.compile('.*\.pyx$'), re.compile('.*\.pxi$'), re.compile('^__pycache__$'),
        re.compile('.*-info$'), re.compile('.*-info$'), re.compile('^EGG_INFO$'),
        re.compile('.*\.so$'), re.compile('^\.DS_Store$')
    ]

    def write_pdy_to_file(python_major, python_minor, python_patch, source_dir,
                          include_dir, python_library, standard_library_dir):
        from lxml import etree

        def package_content(path):
            def is_excluded(x):
                for exclusion_element in exclusion_list:
                    if exclusion_element.search(x):
                        return True

            name = os.path.basename(os.path.normpath(path))
            node = etree.Element('PackageContent')
            node.set('name', name)
            node.set('included', "1")
            if os.path.isfile(path):
                node.set('isdirectory', '0')
            else:
                node.set('isdirectory', '1')
                for file in os.listdir(path):
                    if not is_excluded(file):
                        node.append(package_content(os.path.join(path, file)))
            return node

        project = etree.Element("Project")
        project.set('version', "6")

        python = etree.SubElement(project, "Python")
        python.set('hostinterpreter', '')
        python.set('major', '{}'.format(python_major))
        python.set('minor', '{}'.format(python_minor))
        python.set('patch', '{}'.format(python_patch))
        python.set('platformpython', "linux-* macx win32")
        python.set('sourcedir', source_dir)
        python.set('ssl', "0")
        python.set('targetincludedir', include_dir)
        python.set('targetlibrary', python_library)
        python.set('targetstdlibdir', standard_library_dir)

        application = etree.SubElement(project, "Application")
        application.set('entrypoint', "")
        application.set('isbundle', "1")
        application.set('isconsole', "0")
        application.set('ispyqt5', "1")
        application.set('name', "Genial")
        application.set('script', "genial.py")
        application.set('syspath', "")

        package = etree.SubElement(application, "Package")
        package.set('name', ".")
        package.append(package_content('genial'))
        genial_py_file = etree.SubElement(package, "PackageContent")
        genial_py_file.set('name', 'genial.py')
        genial_py_file.set('included', "1")
        genial_py_file.set('isdirectory', "0")
        license_file = etree.SubElement(package, "PackageContent")
        license_file.set('name', 'LICENSE')
        license_file.set('included', "1")
        license_file.set('isdirectory', "0")

        exclude_pyc = etree.SubElement(package, "Exclude")
        exclude_pyc.set('name', "*.pyc")
        exclude_pyd = etree.SubElement(package, "Exclude")
        exclude_pyd.set('name', "*.pyd")
        exclude_pyo = etree.SubElement(package, "Exclude")
        exclude_pyo.set('name', "*.pyo")
        exclude_pyx = etree.SubElement(package, "Exclude")
        exclude_pyx.set('name', "*.pyx")
        exclude_pxi = etree.SubElement(package, "Exclude")
        exclude_pxi.set('name', "*.pxi")
        exclude_pycache = etree.SubElement(package, "Exclude")
        exclude_pycache.set('name', "__pycache__")
        exclude_info = etree.SubElement(package, "Exclude")
        exclude_info.set('name', "*-info")
        exclude_egginfo = etree.SubElement(package, "Exclude")
        exclude_egginfo.set('name', "EGG_INFO")
        exclude_so = etree.SubElement(package, "Exclude")
        exclude_so.set('name', "*.so")

        pyqtmodule_sip = etree.SubElement(project, "PyQtModule")
        pyqtmodule_sip.set('name', "sip")
        pyqtmodule_qtcore = etree.SubElement(project, "PyQtModule")
        pyqtmodule_qtcore.set('name', "QtCore")
        pyqtmodule_qtwidgets = etree.SubElement(project, "PyQtModule")
        pyqtmodule_qtwidgets.set('name', "QtWidgets")
        pyqtmodule_qtgui = etree.SubElement(project, "PyQtModule")
        pyqtmodule_qtgui.set('name', "QtGui")

        others = etree.SubElement(project, "Others")
        others.set('builddir', "build")
        others.set('qmake', "$SYSROOT/qt-5.5.1/bin/qmake")

        with open(target_pdy, 'wb') as f:
            f.write(etree.tostring(project, pretty_print=True, xml_declaration=True, encoding='utf-8'))

    return {
        'actions': [check_lxml, check_pyqtdeploycli, write_pdy_to_file],
        'params': [
            {
                'name': 'python_major',
                'long': 'python-major',
                'type': int,
                'default': default_python_major,
                'help': 'Python major release to use.'
            },
            {
                'name': 'python_minor',
                'long': 'python-minor',
                'type': int,
                'default': default_python_minor,
                'help': 'Python minor release to use.'
            },
            {
                'name': 'python_patch',
                'long': 'python-patch',
                'type': int,
                'default': default_python_patch,
                'help': 'Python patch release to use.'
            },
            {
                'name': 'source_dir',
                'long': 'source-dir',
                'type': str,
                'default': default_source_dir,
                'help': 'Python source directory.'
            },
            {
                'name': 'include_dir',
                'long': 'include-dir',
                'type': str,
                'default': default_include_dir,
                'help': 'Target include directory.'
            },
            {
                'name': 'python_library',
                'long': 'python-library',
                'type': str,
                'default': default_python_library,
                'help': 'Target Python library.'
            },
            {
                'name': 'standard_library_dir',
                'long': 'standard-library-dir',
                'type': str,
                'default': default_standard_library_dir,
                'help': 'Target standard library directory.'
            }
        ],
        'targets': [target_pdy],
        'verbosity': 2
    }
