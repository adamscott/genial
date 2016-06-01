"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QDir, pyqtSlot
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from genial.ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.set_icons()
        self.set_slots()
        # There is no document opened, so...
        self.set_document_related_widgets_disabled(True)

    # noinspection PyCallByClass,PyTypeChecker
    def set_icons(self):
        self.ui.action_new.setIcon(
            QIcon.fromTheme(
                'document-new',
                QIcon(':/icon/document-new')
            )
        )
        self.ui.action_open.setIcon(
            QIcon.fromTheme(
                'document-open',
                QIcon(':/icon/document-open')
            )
        )
        self.ui.action_save.setIcon(
            QIcon.fromTheme(
                'document-save',
                QIcon(':/icon/document-save')
            )
        )
        self.ui.action_saveas.setIcon(
            QIcon.fromTheme(
                'document-save-as',
                QIcon(':/icon/document-save-as')
            )
        )
        self.ui.action_quit.setIcon(
            QIcon.fromTheme(
                'document-quit',
                QIcon(':/icon/document-quit')
            )
        )
        self.ui.action_undo.setIcon(
            QIcon.fromTheme(
                'document-undo',
                QIcon(':/icon/document-undo')
            )
        )
        self.ui.action_redo.setIcon(
            QIcon.fromTheme(
                'document-redo',
                QIcon(':/icon/document-redo')
            )
        )

    def set_slots(self):
        self.ui.document_widget.document_available.connect(
            self.on_document_widget_document_available
        )
        self.ui.document_widget.document_unavailable.connect(
            self.on_document_widget_document_unavailable
        )

    def set_document_related_widgets_disabled(self, disabled:bool):
        self.ui.action_save.setDisabled(disabled)
        self.ui.action_saveas.setDisabled(disabled)
        self.ui.action_newuser.setDisabled(disabled)
        self.ui.action_removeuser.setDisabled(disabled)
        if disabled:
            # Here, we KNOW that there is no undo/redo
            # when there is no document.
            self.ui.action_undo.setDisabled(True)
            self.ui.action_redo.setDisabled(True)

    def closeEvent(self, event:QCloseEvent):
        if self.ui.document_widget.close_file():
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def on_action_new_triggered(self):
        self.ui.document_widget.new_file()

    @pyqtSlot()
    def on_action_open_triggered(self):
        self.ui.document_widget.open_file()

    @pyqtSlot()
    def on_action_save_triggered(self):
        self.ui.document_widget.save_file()

    @pyqtSlot()
    def on_action_saveas_triggered(self):
        self.ui.document_widget.save_file_as()

    @pyqtSlot()
    def on_action_quit_triggered(self):
        print('Let\'s quit!')

    @pyqtSlot()
    def on_action_newuser_triggered(self):
        print('New user!')

    @pyqtSlot()
    def on_action_removeuser_triggered(self):
        print('Remove user.')

    @pyqtSlot()
    def on_document_widget_document_available(self):
        self.set_document_related_widgets_disabled(False)

    @pyqtSlot()
    def on_document_widget_document_unavailable(self):
        self.set_document_related_widgets_disabled(True)
