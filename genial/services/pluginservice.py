"""

"""
from typing import Union
import tempfile
import shutil
import logging

from PyQt5.QtCore import QObject, QFile, QIODevice, QTextStream, pyqtSlot
from PyQt5.QtWidgets import qApp
from appdirs import *
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager
from yapsy.PluginManager import PluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager, VersionedPluginInfo
from yapsy.PluginInfo import PluginInfo

from genial.utils import debug, logger, logging_level
from genial.plugins import IQuestionPlugin


class PluginService(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._init_plugin_manager()
        self._connect_slots()

    def _connect_slots(self):
        from genial.services import document_service
        qApp.aboutToQuit.connect(
            self.dispose
        )
        document_service.document_created.connect(
            self._activate_document_plugins
        )
        document_service.document_about_to_close.connect(
            self._deactivate_document_plugins
        )

    def _init_plugin_manager(self):
        self.categories = {
            IQuestionPlugin: 'Question'
        }
        filter = {}
        for iplugin, name in self.categories.items():
            filter[name] = iplugin
        plugins_dir = "{}/plugins".format(
            user_data_dir(
                appname="Génial",
                appauthor="Génial"
            )
        )
        os.makedirs(plugins_dir, exist_ok=True)
        self.bundled_plugins_dir = _install_bundled_plugins()  # type: str
        logging.getLogger('yapsy').setLevel(logging_level)
        self.plugin_manager = _setup_plugin_manager(
            self.bundled_plugins_dir,
            plugins_dir,
            filter
        )
        self.plugin_manager.collectPlugins()
        _cat = self.categories[IQuestionPlugin]
        _iterator = iter(self.plugin_manager.getPluginsOfCategory(_cat))
        for plugin_info in _iterator:  # type: Union[PluginInfo,VersionedPluginInfo]
            logging.getLogger(plugin_info.name).setLevel(logging_level)

    @pyqtSlot()
    def dispose(self):
        for plugin_info in self.plugin_manager.getAllPlugins():
            self.plugin_manager.deactivatePluginByName(
                plugin_info.name,
                plugin_info.category
            )
        shutil.rmtree(self.bundled_plugins_dir)

    @pyqtSlot()
    def _activate_document_plugins(self):
        from genial.services import document_service
        self.plugin_manager.updatePluginPlaces([
            document_service.document_plugin_directory
        ])
        self.plugin_manager.collectPlugins()
        _qst_cat = self.categories[IQuestionPlugin]
        _iterator = iter(self.plugin_manager.getPluginsOfCategory(_qst_cat))
        for plugin_info in _iterator:  # type: Union[PluginInfo,VersionedPluginInfo]
            if not plugin_info.is_activated:
                self.plugin_manager.activatePluginByName(
                    plugin_info.name,
                    category=plugin_info.category
                )

    @pyqtSlot()
    def _deactivate_document_plugins(self):
        _qst_cat = self.categories[IQuestionPlugin]
        _iterator = iter(self.plugin_manager.getPluginsOfCategory(_qst_cat))
        for plugin_info in _iterator:  # type: Union[PluginInfo,VersionedPluginInfo]
            if plugin_info.is_activated:
                self.plugin_manager.deactivatePluginByName(
                    plugin_info.name,
                    category=plugin_info.category
                )

    def available_plugins(self, category=None):
        _output = []
        if category is None:
            _iterator = iter(self.plugin_manager.getAllPlugins())
        else:
            _cat = self.categories[category]
            _iterator = iter(self.plugin_manager.getPluginsOfCategory(_cat))
        for plugin_info in _iterator:  # type: Union[PluginInfo,VersionedPluginInfo]
            if plugin_info.is_activated:
                _output.append(plugin_info)
        return _output

    def embedded_plugins(self, category=None):
        from genial.services import document_service
        _output = []
        _plugin_info_list = self.available_plugins(category=category)
        for _plugin_info in _plugin_info_list:
            if document_service.document_plugin_directory is not None:
                _document_plugin_path = document_service.document_plugin_directory
                if _document_plugin_path in _plugin_info.path:
                    _output.append(_plugin_info)
        return _output

    @property
    def available_question_plugins(self):
        return self.available_plugins(category=IQuestionPlugin)

    @property
    def embedded_question_plugins(self):
        return self.embedded_plugins(category=IQuestionPlugin)


def _setup_plugin_manager(bundled_plugins_dir, plugins_dir, categories):
    plugin_manager = PluginManager(
        plugin_info_ext='genial-plugin',
        directories_list=[bundled_plugins_dir, plugins_dir],
        categories_filter=categories
    )
    plugin_manager = AutoInstallPluginManager(
        plugin_install_dir=plugins_dir,
        decorated_manager=plugin_manager
    )
    plugin_manager = VersionedPluginManager(
        decorated_manager=plugin_manager
    )
    return plugin_manager


def _install_bundled_plugins():
    plugin_dir = tempfile.mkdtemp()
    plugin_file_list = [
        'basic/basic.genial-plugin',
        'basic/basic.py'
    ]
    for plugin_file in plugin_file_list:
        base_name = os.path.basename(plugin_file)
        plugin_path = plugin_file.replace(base_name, "")
        plugin_dir_install_path = "{}/{}".format(plugin_dir, plugin_path)
        plugin_file_install_path = "{}/{}".format(plugin_dir, plugin_file)
        if plugin_path:
            os.makedirs(
                plugin_dir_install_path,
                exist_ok=True
            )
        plugin_file_content = _get_file_content(plugin_file)
        with open(plugin_file_install_path, "w+") as f:
            f.write(plugin_file_content)
            f.close()
    return plugin_dir


def _get_file_content(plugin_file):
    name = ':/plugins/{}'.format(plugin_file)
    file = QFile(name)
    if file.open(QIODevice.ReadOnly | QIODevice.Text):
        file_content = ""  # type: str
        text_stream = QTextStream(file)
        while not text_stream.atEnd():
            file_content += text_stream.readLine() + "\n"
        file.close()
        return file_content
    else:
        return None
