import re
from pybuilder.core import init, use_plugin, task, description, depends, Project, Logger
from pybuilder.utils import assert_can_execute, execute_command, discover_files
from pybuilder.errors import BuildFailedException

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
    project.set_property('coverage_exceptions', [
        'genial.ui'
    ])
    project.set_property('genial_localisations', [
        'fr'
    ])
    pass


@task
@description("Compiles .ui files using pyuic5")
def compile_ui(project: Project, logger: Logger):
    logger.info("Compiling .ui files.")
    assert_can_execute(["pyuic5", "--version"],
                       prerequisite="pyuic (PyQt5)",
                       caller="genial build file.")
    compile_generic("{}/src/main/python".format(project.basedir),
                    'pyuic5',
                    '.ui',
                    r'((.*/)(.*)).ui',
                    r'\2ui_\3.py',
                    options="--from-imports")


@task
@depends('compile_ts')
@description("Compiles .qrc files using pyrcc5")
def compile_qrc(project: Project, logger: Logger):
    logger.info("Compiling .qrc files.")
    assert_can_execute(["pyrcc5", "--version"],
                       prerequisite="pyrcc5 (PyQt5)",
                       caller="genial build file.")
    compile_generic("{}/src/main/python".format(project.basedir),
                    'pyrcc5',
                    '.qrc',
                    r'(.*)/resources/(.*).qrc',
                    r'\1/ui/\2_rc.py')

@task
@depends('update_localisation')
@description('Compiles .ts files to .qm using lrelease')
def compile_ts(project: Project, logger:Logger):
    logger.info("Compiling .ts files.")
    assert_can_execute(["lrelease", "--version"],
                       prerequisite="lupdate (Qt5)",
                       caller="genial build file.")
    compile_generic("{}/src/main/python/genial/ui/locale".format(project.basedir),
                    'lrelease',
                    '.ts')


def compile_generic(basedir: str, compiler: str,
                    file_extension: str, pattern_find: re=None,
                    pattern_replace: re=None, output_command="-o",
                    error_file_name="", options=""):
    import os
    import tempfile

    error_file = tempfile.NamedTemporaryFile()

    files = discover_files(basedir, file_extension)
    for file in files:
        if pattern_find and pattern_replace:
            output = re.sub(pattern_find, pattern_replace, file)
        else:
            output = ""
        exit_code = execute_command(
            "{} {} {} {} {}".format(compiler, options, file, output_command, output),
            shell=True,
            error_file_name=error_file.name
        )
        if exit_code != 0:
            raise_error(
                error_file.name,
                "{} failed to compile {}. It returned this error:".format(
                    compiler,
                    file
                )
            )


def raise_error(error_file_name:str, message:str):
    with open(error_file_name, 'r') as f:
        error_message = f.read()
        f.close()
    raise BuildFailedException(message + "\n" + error_message)


@task
@description("Updates the localisation files.")
def update_localisation(project: Project, logger: Logger):
    import re
    import tempfile

    logger.info("Generating .ts files.")
    assert_can_execute(["pylupdate5", "--version"],
                       prerequisite="pylupdate5 (PyQt5)",
                       caller="genial build file.")
    sources = []
    forms = []
    translations = []

    files = discover_files("{}/src/main/python".format(project.basedir), ".py")
    for file in files:
        if not (re.match(r'(.*/)ui_(.*).py', file) or re.match(r'(.*/)__init__\.py', file)):
            sources.append(file)

    files = discover_files("{}/src/main/python".format(project.basedir), ".ui")
    for file in files:
        forms.append(file)

    localisations = project.get_property('genial_localisations')
    for localisation in localisations:
        translations.append(
            "{}/src/main/python/genial/ui/locale/genial_{}.ts".format(
                project.basedir,
                localisation
            )
        )

    tmp_pro_file = tempfile.NamedTemporaryFile()
    with open(tmp_pro_file.name, 'w') as f:
        f.write(create_pro_content("SOURCES = ", sources))
        f.write(create_pro_content("FORMS = ", forms))
        f.write(create_pro_content("TRANSLATIONS = ", translations))
        f.close()

    error_file = tempfile.NamedTemporaryFile()
    exit_code = execute_command("pylupdate5 {}".format(tmp_pro_file.name),
                                error_file_name=error_file.name,
                                shell=True)
    if exit_code != 0:
        message = "pylupdate5 failed to create localisation files. It returned this error:"
        raise_error(error_file.name, message)
    else:
        with open(tmp_pro_file.name, 'r') as f:
            logger.info("Here is the generated genial.pro file: \n{}".format(f.read()))
            f.close()


def create_pro_content(header: str, elements: list) -> str:
    value = header
    elements_len = len(elements)
    i = 0
    for element in elements:
        i += 1
        escape_newline = ""
        if i < elements_len: escape_newline = '\\\n'
        value += "{} {}".format(element, escape_newline)
    value += '\n'
    return value
