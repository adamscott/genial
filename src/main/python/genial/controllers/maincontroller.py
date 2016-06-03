"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject

from genial.views.mainview import MainView
from genial.controllers.documentcontroller import DocumentController


class MainController(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.view = None  # type: MainView
        self.document_controller = None  # type: DocumentController

    def start(self):
        self.document_controller = DocumentController(self)
        self.document_controller.view = self.view.ui.document_view
        self.document_controller.start()
