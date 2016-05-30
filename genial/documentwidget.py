"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from genial.ui.ui_documentwidget import Ui_DocumentWidget

class DocumentWidget(QtWidgets.QWidget, Ui_DocumentWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DocumentWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)