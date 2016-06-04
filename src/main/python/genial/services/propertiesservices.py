"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject

from genial.services.documentservice import document_service


class PropertiesService(QObject):
    def __init__(self, parent=None):
        QObject.__init__(parent)

    def open(self):
        if document_service.is_loaded:
            self.load_properties(document_service.properties)

properties_service = PropertiesService()

from genial.resources import icons_rc
from genial.resources import locale_rc
