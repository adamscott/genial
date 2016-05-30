"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QDir, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMdiSubWindow

from genial.questionswidget import QuestionsWidget
from genial.ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.action_New.triggered.connect(self.onActionNewTriggered)
        self.ui.action_Open.triggered.connect(self.onActionOpenTriggered)
        self.ui.action_Save.triggered.connect(self.onActionSaveTriggered)
        self.ui.actionSave_As.triggered.connect(self.onActionSaveAsTriggered)
        self.setIcons()

    # noinspection PyCallByClass,PyTypeChecker
    def setIcons(self):
        self.ui.action_New.setIcon(
            QIcon.fromTheme(
                'document-new',
                QIcon(':/icon/document-new')
            )
        )
        self.ui.action_Open.setIcon(
            QIcon.fromTheme(
                'document-open',
                QIcon(':/icon/document-open')
            )
        )
        self.ui.action_Save.setIcon(
            QIcon.fromTheme(
                'document-save',
                QIcon(':/icon/document-save')
            )
        )
        self.ui.actionSave_As.setIcon(
            QIcon.fromTheme(
                'document-save-as',
                QIcon(':/icon/document-save-as')
            )
        )

    def onActionNewTriggered(self):
        print('onActionNewTriggered')

    def onActionOpenTriggered(self):
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker,PyArgumentList
        fileName = QFileDialog.getOpenFileName(
            self,
            _translate('MainWindow', 'Open document.'),
            QDir.homePath(),
            _translate('MainWindow', 'Génial files (*.gnl)')
        )

    def onActionSaveTriggered(self):
        print('Save...')

    def onActionSaveAsTriggered(self):
        print('Save as...')