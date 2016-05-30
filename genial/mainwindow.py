"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QDir, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from genial.ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.set_icons()

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

    @pyqtSlot()
    def on_action_new_triggered(self):
        print('on_action_new_triggered')

    @pyqtSlot()
    def on_action_open_triggered(self):
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker,PyArgumentList
        fileName = QFileDialog.getOpenFileName(
            self,
            _translate('MainWindow', 'Open document.'),
            QDir.homePath(),
            _translate('MainWindow', 'Génial files (*.gnl)')
        )

    @pyqtSlot()
    def on_action_save_triggered(self):
        print('Save...')

    @pyqtSlot()
    def on_action_saveas_triggered(self):
        print('Save as...')

    @pyqtSlot()
    def on_action_quit_triggered(self):
        print('Let\'s quit!')

    @pyqtSlot()
    def on_action_newuser_triggered(self):
        print('New user!')

    @pyqtSlot()
    def on_action_removeuser_triggered(self):
        print('Remove user.')