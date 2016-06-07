from pybuilder.core import init, use_plugin, task, description, depends, Project, Logger
from pybuilder.utils import assert_can_execute, execute_command, discover_files
from pybuilder.errors import BuildFailedException

from tempfile import NamedTemporaryFile
import re
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("python.pydev")
use_plugin("python.pycharm")
use_plugin("exec")

default_task = ["compile_ui", "compile_qrc", "publish"]


@init
def initialize(project: Project, logger: Logger):
    project.author = "Adam Scott"
    project.url = "https://github.com/adamscott/genial"
    project.license = "GPL3"
    project.version = "0.1.0"
    project.build_depends_on('mockito')
    project.build_depends_on('requests')
    project.build_depends_on('lxml')
    project.set_property('coverage_exceptions', [
        'genial.ui'
    ])
    project.set_property('genial_localisations', [
        'fr'
    ])


@task
@description("Compiles .ui files using pyuic5")
def compile_ui(project: Project, logger: Logger):
    logger.info("Compiling .ui files.")
    assert_can_execute(["pyuic5", "--version"],
                       prerequisite="pyuic (PyQt5)",
                       caller="genial build file.")

    source_dir = "{}/src/main/python".format(project.basedir)
    error_file = NamedTemporaryFile()

    files_names = discover_files("{}/genial/ui".format(source_dir), ".ui")
    for file_name in files_names:
        base_name = os.path.basename(file_name)
        output_base_name = re.sub(r'(.*)\.ui', r'ui_\1\.py', base_name)
        exit_code = execute_command(
            "pyuic5 {} {} -o {}".format(
                "--import-from=genial.resources",
                file_name,
                "{}/genial/views/gen/{}".format(source_dir, output_base_name)
            ),
            shell=True,
            error_file_name=error_file.name
        )
        if exit_code != 0:
            raise_error(error_file.name, "pyuic5 returned an error:")


@task
@depends('generate_locale_qrc', 'generate_icons_qrc')
@description("Compiles .qrc files using pyrcc5")
def compile_qrc(project: Project, logger: Logger):
    logger.info("Compiling .qrc files.")
    assert_can_execute(["pyrcc5", "--version"],
                       prerequisite="pyrcc5 (PyQt5)",
                       caller="genial build file.")

    source_dir = "{}/src/main/python".format(project.basedir)
    error_file = NamedTemporaryFile()

    files_names = discover_files("{}/genial/resources".format(source_dir), ".qrc")
    for file_name in files_names:
        base_name = os.path.basename(file_name)
        output_base_name = re.sub(r'(.*)\.qrc', r'\1_rc\.py', base_name)
        exit_code = execute_command(
            "pyrcc5 {} -o {}".format(
                file_name,
                "{}/genial/resources/{}".format(source_dir, output_base_name)
            ),
            shell=True,
            error_file_name=error_file.name
        )
        if exit_code != 0:
            raise_error(error_file.name, "pyrcc5 returned an error:")


@task
@depends('compile_ts')
@description('Generates a .qrc file based on the .qm files in the locale directory')
def generate_locale_qrc(project: Project, logger: Logger):
    logger.info("Generating locale .qrc file.")
    source_dir = "{}/src/main/python".format(project.basedir)
    resources_dir = "{}/genial/resources".format(source_dir)

    generated_qrc = "<RCC>"
    generated_qrc += '\n  <qresource prefix="/locale">'

    files = discover_files("{}/locale".format(resources_dir), ".qm")
    for file in files:
        base_name = os.path.basename(file)
        generated_qrc += '\n    <file alias="{}">locale/{}</file>'.format(
            base_name, base_name
        )

    generated_qrc += "\n  </qresource>"
    generated_qrc += "\n</RCC>\n"

    with open('{}/locale.qrc'.format(resources_dir), 'w+') as f:
        f.write(generated_qrc)
        f.close()


@task
@depends('download_icons')
@description('Generates a .qrc file based on the icons in the resources directory')
def generate_icons_qrc(project: Project, logger: Logger):
    logger.info("Generating locale .qrc file.")
    source_dir = "{}/src/main/python".format(project.basedir)
    resources_dir = "{}/genial/resources".format(source_dir)

    generated_qrc = "<RCC>"
    generated_qrc += '\n  <qresource prefix="/icons">'

    files = discover_files("{}/icons".format(resources_dir), ".svg")
    number_of_files = 0
    for file in files:
        number_of_files += 1
        base_name = os.path.basename(file)
        generated_qrc += '\n    <file alias="{}">icons/{}</file>'.format(
            base_name, base_name
        )

    generated_qrc += "\n  </qresource>"
    generated_qrc += "\n</RCC>\n"

    # As it's not sure that any icon is there
    # pyrcc5 doesn't like empty .qrc files
    if number_of_files > 0:
        with open('{}/icons.qrc'.format(resources_dir), 'w+') as f:
            f.write(generated_qrc)
            f.close()


@task
@depends('update_ts')
@description('Compiles .ts files to .qm using lrelease')
def compile_ts(project: Project, logger: Logger):
    logger.info("Compiling .ts files.")
    assert_can_execute(["lrelease", "--version"],
                       prerequisite="lupdate (Qt5)",
                       caller="genial build file.")

    source_dir = "{}/src/main/python".format(project.basedir)
    error_file = NamedTemporaryFile()

    files_names = discover_files("{}/genial/resources/locale".format(source_dir), ".ts")
    for file_name in files_names:
        base_name = os.path.basename(file_name)
        output_base_name = re.sub(r'(.*)\.ts', r'\1\.qm', base_name)
        exit_code = execute_command(
            "lrelease {} -qm {}".format(
                file_name,
                "{}/genial/resources/locale/{}".format(
                    source_dir,
                    output_base_name
                )
            ),
            shell=True,
            error_file_name=error_file.name
        )
        if exit_code != 0:
            raise_error(error_file.name, "lrelease returned an error:")


@task
@description("Updates the localisation files.")
def update_ts(project: Project, logger: Logger):
    def create_pro_content(header: str, elements: list) -> str:
        value = header
        elements_len = len(elements)
        i = 0
        for element in elements:
            i += 1
            escape_newline = ""
            if i < elements_len:
                escape_newline = '\\\n'
            value += "{} {}".format(element, escape_newline)
        value += '\n'
        return value

    logger.info("Generating .ts files.")
    assert_can_execute(["pylupdate5", "--version"],
                       prerequisite="pylupdate5 (PyQt5)",
                       caller="genial build file.")
    sources = []
    forms = []
    translations = []

    source_dir = "{}/src/main/python".format(project.basedir)

    files = discover_files(source_dir, ".py")
    for file in files:
        if not (re.match(r'(.*/)ui_(.*).py', file) or re.match(r'(.*/)__init__\.py', file)):
            sources.append(file)

    files = discover_files("{}/genial/ui".format(source_dir), ".ui")
    for file in files:
        forms.append(file)

    localisations = project.get_property('genial_localisations')
    for localisation in localisations:
        ts_file_path = "{}/src/main/python/genial/resources/locale/genial_{}.ts".format(
            project.basedir,
            localisation
        )
        translations.append(ts_file_path)
        # Creates the file if it doesn't not exist.
        with open(ts_file_path, 'a+') as f:
            f.close()

    tmp_pro_file = NamedTemporaryFile()
    with open(tmp_pro_file.name, 'w') as f:
        f.write(create_pro_content("SOURCES = ", sources))
        f.write(create_pro_content("FORMS = ", forms))
        f.write(create_pro_content("TRANSLATIONS = ", translations))
        f.close()

    error_file = NamedTemporaryFile()
    exit_code = execute_command(
        "pylupdate5 {} {}".format(
            "-translate-function _translate",
            tmp_pro_file.name
        ),
        error_file_name=error_file.name,
        shell=True
    )

    if exit_code != 0:
        tmp_pro_file.close()
        message = "pylupdate5 failed to create localisation files. It returned this error:"
        raise_error(error_file.name, message)
    else:
        with open(tmp_pro_file.name, 'r') as f:
            logger.info("Here is the generated genial.pro file: \n{}".format(f.read()))
            f.close()
            tmp_pro_file.close()


@task
@description("Generates a .qm from Qt for each language defined.")
def generate_qt_qm(project: Project, logger: Logger):
    import requests
    logger.info("Generating .qm file from Qt.")
    assert_can_execute(["pylupdate5", "--version"],
                       prerequisite="pylupdate5 (PyQt5)",
                       caller="genial build file.")
    languages = project.get_property('genial_localisations')
    qt_files_needed = [
        'qtbase'
    ]
    source_dir = "{}/src/main/python".format(project.basedir)
    for language in languages:
        logger.info("Getting .ts files for {}.".format(language))
        files_downloaded = []
        for qt_file_needed in qt_files_needed:
            file = NamedTemporaryFile()
            response = requests.get(
                'http://l10n-files.qt.io' +
                '/l10n-files/qt5-current/{}_{}.ts'.format(
                    qt_file_needed,
                    language
                )
            )
            if response.status_code == 200:
                file.write(response.text)
                files_downloaded.append(file)

        error_file = NamedTemporaryFile()
        exit_code = execute_command(
            "lrelease {} -qm {}".format(
                " ".join([f.name for f in files_downloaded]),
                "{}/genial/resources/locale/qt_{}.qm".format(
                    source_dir,
                    language
                )
            ),
            error_file_name=error_file.name,
            shell=True
        )
        if exit_code != 0:
            message = "lrelease failed to join localisation files. It returned this error:"
            raise_error(error_file.name, message)


@task
@description("Download icons for Windows/Mac from the GNOME desktop icons.")
def download_icons(project: Project, logger: Logger):
    from lxml import html
    import requests
    logger.info("Downloading icons files from GNOME Desktop icons.")
    source_dir = "{}/src/main/python".format(project.basedir)
    icons_dir = "{}/genial/resources/icons".format(source_dir)
    needed_icons = [
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

    for needed_icon in needed_icons:
        logger.info('Downloading "{}" icon.'.format(needed_icon))
        file_page = requests.get(
            "https://commons.wikimedia.org/wiki/File:Gnome-{}.svg".format(
                needed_icon
            )
        )
        file_tree = html.fromstring(file_page.content)
        svg_url = file_tree.xpath('//div[@class="fullImageLink"]/a/@href')
        if len(svg_url) > 0:
            svg_page = requests.get(svg_url[0])
            os.makedirs(icons_dir, exist_ok=True)
            with open('{}/{}.svg'.format(icons_dir, needed_icon), '+w') as f:
                f.write(svg_page.text)
        else:
            raise FileNotFoundError("No link was found for '{}'.".format(
                needed_icon
            ))


def raise_error(error_file_name: str, message: str):
    with open(error_file_name, 'r') as f:
        error_message = f.read()
        f.close()
    raise BuildFailedException(message + "\n" + error_message)
