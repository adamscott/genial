"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
__author__ = 'Adam Scott'
__author_email__ = "ascott.ca@gmail.com"
__license__ = 'GPL3'

from .documentservice import DocumentService
from .pluginservice import PluginService
from .propertiesservices import PropertiesService

document_service = DocumentService()  # type: DocumentService
plugin_service = PluginService()  # type: PluginService
properties_service = PropertiesService()  # type: PropertiesService
