from pybuilder.core import init, use_plugin, task, description, Project, Logger

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("python.pydev")
use_plugin("python.pycharm")
use_plugin("exec")

default_task = "publish"

@init
def initialize(project:Project):
    project.build_depends_on('mockito')

@task
@description("Compiles .ui files using pyuic5")
def compile_ui(project:Project, logger:Logger):
    logger.debug("Compiling ui.")

@task
@description("Compiles .qrc files using pyrcc5")
def compile_qrc(project:Project, logger:Logger):
    logger.debug("Compiling qrc.")