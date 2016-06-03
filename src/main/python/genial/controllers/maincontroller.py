"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication

from genial.views.mainview import *
from genial.controllers.documentcontroller import *


class MainController(QObject):
    view = None  # type: MainView
    document_controller = None  # type: DocumentController

    def start(self):
        if self.view is None:
            self.view = MainView()
        self.connect_slots()
        self.view.show()
        self.document_controller = DocumentController(self)
        self.document_controller.view = self.view.ui.document_view
        self.document_controller.start()

    def connect_slots(self):
        self.view.ui.action_new.triggered.connect(
            self.on_action_new_triggered
        )

    @pyqtSlot()
    def on_action_new_triggered(self):
        self.document_controller.request_new_document()
