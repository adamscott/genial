"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from typing import List, Dict, Optional, Union

from PyQt5.QtCore import QObject
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager
from yapsy.PluginManager import PluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager, VersionedPluginInfo
from yapsy.PluginInfo import PluginInfo
from yapsy.IPlugin import IPlugin

DecoratedManager = Union[PluginManager,AutoInstallPluginManager,VersionedPluginManager]
DecoratedPluginInfo = Union[PluginInfo, VersionedPluginInfo]


class PluginService(QObject):
    plugin_manager = ...  # type: DecoratedManager
    bundled_plugins_dir = ...  # type: str
    categories = ...  # type: Dict[IPlugin, str]

    def __init__(self) -> None: ...
    def _connect_slots(self) -> None: ...
    def _init_plugin_manager(self) -> None: ...
    def dispose(self) -> None: ...
    def _activate_document_plugins(self) -> None: ...
    def _deactivate_document_plugins(self) -> None: ...
    def available_plugins(self, category: IPlugin = None) -> List[DecoratedPluginInfo]: ...
    def embedded_plugins(self, category: IPlugin = None) -> List[DecoratedPluginInfo]: ...
    def available_question_plugins(self) -> List[DecoratedPluginInfo]: ...
    def embedded_question_plugins(self) -> List[DecoratedPluginInfo]: ...


def _setup_plugin_manager(bundled_plugins_dir,  # type: str
                          plugins_dir,  # type: str
                          categories  # type: Dict[str, IPlugin]
                          ) -> DecoratedManager:
def _install_bundled_plugins() -> str: ...
def _get_file_content(plugin_file: str) -> Optional[str]: ...
