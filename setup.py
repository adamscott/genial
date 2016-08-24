# !/usr/bin/env python
from setuptools import setup
from setuptools import Command
from setuptools.command.test import test as TestCommand
from tempfile import NamedTemporaryFile
import io
import os
import re
import subprocess
import shutil
import sys
import urllib.request

here = os.path.abspath(os.path.dirname(__file__))


def read(*file_names, **kwargs):
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in file_names:
        with io.open(filename) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'CHANGES.rst')


class CompileUI(Command):
    user_options = [('pyuic5=', 'b', 'Alternate path for "pyuic5"')]

    def initialize_options(self):
        self.pyuic5 = None

    def finalize_options(self):
        if not self.pyuic5:
            self.pyuic5 = "pyuic5"
        if not shutil.which(self.pyuic5):
            sys.exit("'{}' command not found. Is PyQt5 well installed?".format(self.pyuic5))

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        ui_dir = "{}/genial/ui".format(root_dir)
        gen_dir = "{}/genial/views/gen".format(root_dir)
        for file in os.listdir(ui_dir):
            if file.endswith(".ui"):
                output_file = re.sub(r'(.*)\.ui', r'ui_\1.py', file)
                command = " ".join([
                    self.pyuic5,
                    "--import-from=genial.resources",
                    "{}/{}".format(ui_dir, file),
                    "-o {}/{}".format(gen_dir, output_file)
                ])
                ret_code = subprocess.call(command, shell=True)
                if ret_code != 0:
                    sys.exit("'pyuic5' command failed. ({})".format(command))


class CompileQRC(Command):
    user_options = [('pyrcc5=', 'b', 'Alternate path for "pyrcc5"')]

    def initialize_options(self):
        self.pyrcc5 = None

    def finalize_options(self):
        if not self.pyrcc5:
            self.pyrcc5 = "pyrcc5"
        if not shutil.which(self.pyrcc5):
            sys.exit("'{}' command not found. Is PyQt5 well installed?".format(self.pyrcc5))

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = "{}/genial/resources".format(root_dir)
        for file in os.listdir(resources_dir):
            if file.endswith(".qrc"):
                output_file = re.sub(r'(.*)\.qrc', r'\1_rc.py', file)
                command = " ".join([
                    self.pyrcc5,
                    "{}/{}".format(resources_dir, file),
                    "-o {}/{}".format(resources_dir, output_file)
                ])
                ret_code = subprocess.call(command, shell=True)
                if ret_code != 0:
                    sys.exit("'pyrcc5' command failed. ({})".format(command))


class GenerateLocale(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = "{}/genial/resources".format(root_dir)
        locale_dir = "{}/genial/resources/locale".format(root_dir)
        qrc_content = "<RCC>"
        qrc_content += '\n  <qresource prefix="/locale">'
        file_found = False
        for file in os.listdir(locale_dir):
            if file.endswith(".qm"):
                file_found = True
                qrc_content += "\n    <file alias='{}'>locale/{}</file>".format(file, file)
        qrc_content += "\n  </qresource>"
        qrc_content += "\n</RCC>\n"
        if file_found:
            with open("{}/locale.qrc".format(resources_dir), 'w+') as f:
                f.write(qrc_content)
                f.close()


class GenerateIcons(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = "{}/genial/resources".format(root_dir)
        icons_dir = "{}/genial/resources/icons".format(root_dir)
        qrc_content = "<RCC>"
        qrc_content += '\n  <qresource prefix="/icons">'
        file_found = False
        for file in os.listdir(icons_dir):
            if file.endswith(".svg"):
                file_found = True
                qrc_content += "\n    <file alias='{}'>icons/{}</file>".format(file, file)
        qrc_content += "\n  </qresource>"
        qrc_content += "\n</RCC>\n"
        if file_found:
            with open("{}/icons.qrc".format(resources_dir), 'w+') as f:
                f.write(qrc_content)
                f.close()


class GeneratePlugins(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = "{}/genial/resources".format(root_dir)
        plugins_dir = "{}/genial/resources/plugins".format(root_dir)
        qrc_content = "<RCC>"
        qrc_content += '\n  <qresource prefix="/plugins">'
        file_found = False
        os.chdir(resources_dir)
        for root, dirs, files in os.walk("plugins"):
            for file in files:
                if file.endswith(".genial-plugin") or file.endswith(".py"):
                    file_found = True
                    plugins_stripped_root = root.replace("plugins/", "")
                    qrc_content += "\n    <file alias='{}/{}'>{}/{}</file>".format(
                        plugins_stripped_root,
                        file,
                        root,
                        file
                    )

        qrc_content += "\n  </qresource>"
        qrc_content += "\n</RCC>\n"
        if file_found:
            with open("{}/plugins.qrc".format(resources_dir), 'w+') as f:
                f.write(qrc_content)
                f.close()


class UpdateTS(Command):
    user_options = [('pylupdate5=', 'b', 'Alternate path for "pylupdate5"')]

    def initialize_options(self):
        self.pylupdate5 = None

    def finalize_options(self):
        if not self.pylupdate5:
            self.pylupdate5 = "pylupdate5"
        if not shutil.which(self.pylupdate5):
            sys.exit("'{}' command not found. Is PyQt5 well installed?".format(self.pylupdate5))

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.join(root_dir, "genial/")
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
        pro_file_content = "SOURCES = " + " \\\n".join(sources) + "\n"
        pro_file_content += "FORMS = " + " \\\n".join(forms) + "\n"
        pro_file_content += "TRANSLATIONS = " + " \\\n".join(translations)
        print("Here is the generated .pro:")
        print(pro_file_content)
        with NamedTemporaryFile("w+") as pro_file:
            pro_file.write(pro_file_content)
            pro_file.flush()
            command = " ".join([
                self.pylupdate5,
                "-verbose",
                "-translate-function '_translate'",
                pro_file.name
            ])
            print(command)
            ret_code = subprocess.call(command, shell=True)
            if ret_code != 0:
                sys.exit("'pylupdate5' command failed. ({})\nHere is the .pro file generated:\n{}".format(
                    command,
                    pro_file_content
                ))


class DownloadQTBaseTS(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        locale_dir = "{}/genial/resources/locale".format(root_dir)
        languages = []
        for file in os.listdir(locale_dir):
            if file.endswith(".ts"):
                match = re.match(r'genial_(.*)\.ts', file)
                if match is not None:
                    languages.append(match.group(1))
        for language in languages:
            url = "http://l10n-files.qt.io/l10n-files/qt5-old/qtbase_{}.ts".format(language)
            with urllib.request.urlopen(url) as response:
                content = response.read()
                content_file_path = "{}/qtbase_{}.ts".format(locale_dir, language)
                with open(content_file_path, "wb+") as f:
                    f.write(content)
                    f.close()


class GenerateQM(Command):
    user_options = [('lrelease=', 'b', 'Alternate path for "lrelease"')]

    def initialize_options(self):
        self.lrelease = None

    def finalize_options(self):
        if not self.lrelease:
            self.lrelease = "lrelease"
        if not shutil.which(self.lrelease):
            sys.exit("'{}' command not found. Is Qt5 well installed?".format(self.lrelease))

    def run(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        locale_dir = "{}/genial/resources/locale".format(root_dir)
        languages = []
        for file in os.listdir(locale_dir):
            if file.endswith(".ts"):
                match = re.match(r'genial_(.*)\.ts', file)
                if match is not None:
                    languages.append(match.group(1))
        for language in languages:
            genial_ts_file = "{}/genial_{}.ts".format(locale_dir, language)
            genial_qm_file = "{}/genial_{}.qm".format(locale_dir, language)
            qt_ts_file = "{}/qtbase_{}.ts".format(locale_dir, language)
            qt_qm_file = "{}/qtbase_{}.qm".format(locale_dir, language)
            # Compile Genial .qm
            command = " ".join([
                self.lrelease,
                genial_ts_file,
                "-qm {}".format(genial_qm_file)
            ])
            ret_code = subprocess.call(command, shell=True)
            if ret_code != 0:
                sys.exit("'lrelease' command failed while generating '{}'. ({})".format(
                    genial_qm_file,
                    command
                ))
            # Compile QT .qm
            command = " ".join([
                self.lrelease,
                qt_ts_file,
                "-qm {}".format(qt_qm_file)
            ])
            ret_code = subprocess.call(command, shell=True)
            if ret_code != 0:
                sys.exit("'lrelease' command failed while generating '{}'. ({})".format(
                    qt_qm_file,
                    command
                ))


class DownloadIcons(Command):
    user_options = [
        ('icons=', 'i', 'Icons to download, separated by commas.'),
        ('force=', 'f', 'Force download, even if an icon is already present.')
    ]

    def initialize_options(self):
        self.icons = None
        self.force = None

    def finalize_options(self):
        if self.icons:
            self.icons = self.icons.split(",")
        else:
            self.icons = [
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
        if self.force is not None:
            if self.force == "false" or self.force == "False":
                self.force = False
            else:
                self.force = True
        else:
            self.force = False

    def run(self):
        # import here, cause outside the eggs aren't loaded
        from lxml import html
        root_dir = os.path.dirname(os.path.realpath(__file__))
        icons_dir = "{}/genial/resources/icons".format(root_dir)
        for icon in self.icons:
            if not self.force:
                if os.path.isfile('{}/{}.svg'.format(icons_dir, icon)):
                    continue
            file_url = "https://commons.wikimedia.org/wiki/File:Gnome-{}.svg".format(icon)
            with urllib.request.urlopen(file_url) as file_response:
                file_content = file_response.read()
                file_tree = html.fromstring(file_content)
                svg_urls = file_tree.xpath('//div[@class="fullImageLink"]/a/@href')
                if len(svg_urls) > 0:
                    with urllib.request.urlopen(svg_urls[0]) as svg_response:
                        svg_content = svg_response.read()
                        os.makedirs(icons_dir, exist_ok=True)
                        with open('{}/{}.svg'.format(icons_dir, icon), '+wb') as f:
                            f.write(svg_content)
                else:
                    raise FileNotFoundError("No link was found for '{}'.".format(icon))


class Bootstrap(Command):
    user_options = [
        ('pyuic5=', None, 'Alternate path for "pyuic5"'),
        ('pyrcc5=', None, 'Alternate path for "pyrcc5"'),
        ('lrelease=', None, 'Alternate path for "lrelease"'),
        ('pylupdate5=', None, 'Alternate path for "pylupdate5"'),
        ('icons=', 'i', 'Icons to download, separated by commas.'),
        ('force=', 'f', 'Force download, even if an icon is already present.'),
        ('python=', 'p', 'Alternate path for "python"')
    ]

    def initialize_options(self):
        CompileUI.initialize_options(self)
        CompileQRC.initialize_options(self)
        GenerateLocale.initialize_options(self)
        GenerateIcons.initialize_options(self)
        GeneratePlugins.initialize_options(self)
        UpdateTS.initialize_options(self)
        DownloadQTBaseTS.initialize_options(self)
        GenerateQM.initialize_options(self)
        DownloadIcons.initialize_options(self)
        self.python = None

    def finalize_options(self):
        CompileUI.finalize_options(self)
        CompileQRC.finalize_options(self)
        GenerateLocale.finalize_options(self)
        GenerateIcons.finalize_options(self)
        GeneratePlugins.finalize_options(self)
        UpdateTS.finalize_options(self)
        DownloadQTBaseTS.finalize_options(self)
        GenerateQM.finalize_options(self)
        DownloadIcons.finalize_options(self)
        if not self.python:
            self.python = "python"
        if not shutil.which(self.python):
            sys.exit("'{}' command not found.".format(self.python))
        self.setup_path = os.path.realpath(__file__)

    def launch_subprocess(self, command_name, params=None):
        command_params = ""
        if params is not None:
            command_params = " ".join(params)
        command = " ".join([
            self.python,
            self.setup_path,
            command_name,
            command_params
        ])
        ret_code = subprocess.call(command, shell=True)
        if ret_code != 0:
            sys.exit("'setup.py' command failed. ({})".format(command))

    def run(self):
        # Download icons
        icon_param = "--icons=" + ",".join(self.icons)
        force_param = "--force=" + str(self.force)
        self.launch_subprocess("download_icons", [icon_param, force_param])
        # Download QT Base .ts
        self.launch_subprocess("download_qtbase_ts")
        # Update .ts
        pylupdate5_param = "--pylupdate5=" + self.pylupdate5
        self.launch_subprocess("update_ts", [pylupdate5_param])
        # Generate .qm
        lrelease_param = "--lrelease=" + self.lrelease
        self.launch_subprocess("generate_qm", [lrelease_param])
        # Generate locale
        self.launch_subprocess("generate_locale")
        # Generate icons
        self.launch_subprocess("generate_icons")
        # Generate plugins
        self.launch_subprocess("generate_plugins")
        # Compile .qrc
        pyrcc5_param = "--pyrcc5=" + self.pyrcc5
        self.launch_subprocess("compile_qrc", [pyrcc5_param])
        # Compile .ui
        pyuic5_param = "--pyuic5=" + self.pyuic5
        self.launch_subprocess("compile_ui", [pyuic5_param])
        # Convert .md
        pandoc_param = "--pandoc=" + self.pandoc
        self.launch_subprocess("convert_md", [pandoc_param])


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        import sys
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='genial',
    packages=['genial'],
    version='0.1.0',
    description='A "Génies en herbe" questions manager.',
    author='Adam Scott',
    license='GPLv3',
    author_email='ascott.ca@gmail.com',
    url='https://github.com/adamscott/genial',
    keywords=['quiz', 'manager', ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X :: Aqua',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Natural Language :: French',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Education',
        'Topic :: Database'
    ],
    tests_require=['tox'],
    install_requires=['PyQt5', 'yapsy', 'appdirs'],
    setup_requires=['lxml'],
    cmdclass={
        'test': Tox,
        'convert_md': ConvertMD,
        'compile_ui': CompileUI,
        'compile_qrc': CompileQRC,
        'generate_locale': GenerateLocale,
        'generate_icons': GenerateIcons,
        'generate_plugins': GeneratePlugins,
        'update_ts': UpdateTS,
        'download_qtbase_ts': DownloadQTBaseTS,
        'generate_qm': GenerateQM,
        'download_icons': DownloadIcons,
        'bootstrap': Bootstrap
    },
    include_package_data=True,
    extras_require={
        'testing': ['tox'],
    }
)
