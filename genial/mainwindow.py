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
        self.ui.mdiArea.subWindowActivated.connect(self.onSubWindowActivated)
        self.setIcons()
        self.setupNoSubWindow()

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

    def setupNoSubWindow(self):
        self.ui.action_Save.setDisabled(True)
        self.ui.actionSave_As.setDisabled(True)

    def setupHasSubWindow(self):
        self.ui.action_Save.setDisabled(False)
        self.ui.actionSave_As.setDisabled(False)

    def onActionNewTriggered(self):
        self.openDocument()

    def onActionOpenTriggered(self):
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker,PyArgumentList
        fileName = QFileDialog.getOpenFileName(
            self,
            _translate('MainWindow', 'Open document.'),
            QDir.homePath(),
            _translate('MainWindow', 'Génial files (*.gnl)')
        )
        if fileName[0]:
            self.openDocument(fileName)

    def onActionSaveTriggered(self):
        print('Save...')

    def onActionSaveAsTriggered(self):
        print('Save as...')

    def openDocument(self, fileName=None):
        subwindow = QMdiSubWindow(self.ui.mdiArea)
        questionWidget = QuestionsWidget(subwindow)
        questionWidget.open(fileName)
        subwindow.setWidget(questionWidget)
        subwindow.setAttribute(Qt.WA_DeleteOnClose)
        subwindow.show()
        subwindow.destroyed.connect(self.onSubWindowDestroyed)
        questionWidget.show()
        self.ui.mdiArea.addSubWindow(subwindow)
        self.setupHasSubWindow()

    def onSubWindowActivated(self, subwindow):
        '''
        @type subwindow: QMdiSubWindow
        '''
        print('activated')
        print(subwindow)

    def onSubWindowDestroyed(self, subwindow):
        '''
        @type subwindow: QMdiSubWindow
        '''
        print('destroyed')
        print(subwindow)

        list = self.ui.mdiArea.subWindowList() # array[QMdiSubWindow]
        if len(list) == 0:
            self.setupNoSubWindow()
