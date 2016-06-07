"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication

from genial.views.mainview import MainView
from genial.controllers.documentcontroller import DocumentController
from genial.services.documentservice import document_service


class MainController(QObject):
    application = None  # type:QApplication
    view = None  # type: MainView
    document_controller = None  # type: DocumentController

    def __init__(self, parent: QApplication):
        QObject.__init__(self, parent)
        self.application = parent

    def start(self):
        if self.view is None:
            self.view = MainView()
            self.view.show()
        self.connect_slots()
        self.view.set_document_related_widgets_disabled(True)
        self.view.show()
        self.document_controller = DocumentController(self)
        self.document_controller.view = self.view.ui.document_view
        self.document_controller.start()

    def connect_slots(self):
        self.view.action_new_triggered.connect(
            self.on_action_new_triggered
        )
        self.view.action_open_triggered.connect(
            self.on_action_open_triggered
        )
        self.view.action_save_triggered.connect(
            self.on_action_save_triggered
        )
        self.view.action_save_as_triggered.connect(
            self.on_action_save_as_triggered
        )
        self.view.action_close_triggered.connect(
            self.on_action_close_triggered
        )
        self.view.action_quit_triggered.connect(
            self.on_action_quit_triggered
        )
        self.view.action_new_user_triggered.connect(
            self.on_action_new_user_triggered
        )
        self.view.action_remove_user_triggered.connect(
            self.on_action_remove_user_triggered
        )
        document_service.document_created.connect(
            self.on_document_created
        )
        document_service.document_closed.connect(
            self.on_document_closed
        )

    @staticmethod
    def request_quit() -> bool:
        return document_service.close()

    @pyqtSlot()
    def on_action_new_triggered(self):
        document_service.new()

    @pyqtSlot()
    def on_action_open_triggered(self):
        document_service.open()

    @pyqtSlot()
    def on_action_save_triggered(self):
        pass

    @pyqtSlot()
    def on_action_save_as_triggered(self):
        pass

    @pyqtSlot()
    def on_action_close_triggered(self):
        document_service.close()

    @pyqtSlot()
    def on_action_quit_triggered(self):
        self.application.quit()

    @pyqtSlot()
    def on_action_new_user_triggered(self):
        pass

    @pyqtSlot()
    def on_action_remove_user_triggered(self):
        pass

    @pyqtSlot()
    def on_document_created(self):
        self.view.set_document_related_widgets_disabled(False)

    @pyqtSlot()
    def on_document_closed(self):
        self.view.set_document_related_widgets_disabled(True)

from genial.resources import icons_rc
from genial.resources import locale_rc
