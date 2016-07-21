"""

"""
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from genial.views.gen.ui_mainview import Ui_MainView


class MainView(QMainWindow, Ui_MainView):
    action_new_triggered = pyqtSignal()
    action_open_triggered = pyqtSignal()
    action_save_triggered = pyqtSignal()
    action_save_as_triggered = pyqtSignal()
    action_close_triggered = pyqtSignal()
    action_quit_triggered = pyqtSignal()
    action_new_user_triggered = pyqtSignal()
    action_remove_user_triggered = pyqtSignal()
    action_properties_triggered = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.menubar.setNativeMenuBar(False)
        self.set_icons()

    def closeEvent(self, event: QCloseEvent):
        from genial.controllers.maincontroller import MainController
        if MainController.request_quit():
            event.accept()
        else:
            event.ignore()

    # noinspection PyCallByClass,PyTypeChecker
    def set_icons(self):
        self.ui.action_new.setIcon(
            QIcon.fromTheme(
                'document-new',
                QIcon(':/icons/document-new.svg')
            )
        )
        self.ui.action_open.setIcon(
            QIcon.fromTheme(
                'document-open',
                QIcon(':/icons/document-open.svg')
            )
        )
        self.ui.action_save.setIcon(
            QIcon.fromTheme(
                'document-save',
                QIcon(':/icons/document-save.svg')
            )
        )
        self.ui.action_save_as.setIcon(
            QIcon.fromTheme(
                'document-save-as',
                QIcon(':/icons/document-save-as.svg')
            )
        )
        self.ui.action_close.setIcon(
            QIcon.fromTheme(
                'window-close',
                QIcon(':/icons/window-close.svg')
            )
        )
        self.ui.action_quit.setIcon(
            QIcon.fromTheme(
                'application-exit',
                QIcon(':/icons/application-exit.svg')
            )
        )
        self.ui.action_undo.setIcon(
            QIcon.fromTheme(
                'edit-undo',
                QIcon(':/icons/edit-undo.svg')
            )
        )
        self.ui.action_redo.setIcon(
            QIcon.fromTheme(
                'edit-redo',
                QIcon(':/icons/edit-redo.svg')
            )
        )
        self.ui.action_print.setIcon(
            QIcon.fromTheme(
                'document-print',
                QIcon(':/icons/document-print.svg')
            )
        )
        self.ui.action_properties.setIcon(
            QIcon.fromTheme(
                'document-properties',
                QIcon(':/icons/document-properties.svg')
            )
        )

    def set_document_related_widgets_disabled(self, disabled: bool):
        self.ui.action_save.setDisabled(disabled)
        self.ui.action_save_as.setDisabled(disabled)
        self.ui.action_new_user.setDisabled(disabled)
        self.ui.action_remove_user.setDisabled(disabled)
        self.ui.action_properties.setDisabled(disabled)
        self.ui.action_print.setDisabled(disabled)
        self.ui.action_close.setDisabled(disabled)
        if disabled:
            # Here, we KNOW that there is no undo/redo
            # when there is no document.
            self.ui.action_undo.setDisabled(True)
            self.ui.action_redo.setDisabled(True)

    @pyqtSlot()
    def on_action_new_triggered(self):
        self.action_new_triggered.emit()

    @pyqtSlot()
    def on_action_open_triggered(self):
        self.action_open_triggered.emit()

    @pyqtSlot()
    def on_action_save_triggered(self):
        self.action_save_triggered.emit()

    @pyqtSlot()
    def on_action_save_as_triggered(self):
        self.action_save_as_triggered.emit()

    @pyqtSlot()
    def on_action_close_triggered(self):
        self.action_close_triggered.emit()

    @pyqtSlot()
    def on_action_quit_triggered(self):
        self.action_quit_triggered.emit()

    @pyqtSlot()
    def on_action_new_user_triggered(self):
        self.action_new_user_triggered.emit()

    @pyqtSlot()
    def on_action_remove_user_triggered(self):
        self.action_remove_user_triggered.emit()

    @pyqtSlot()
    def on_action_properties_triggered(self):
        self.action_properties_triggered.emit()
