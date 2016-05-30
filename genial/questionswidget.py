"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from genial.ui.ui_questionswidget import Ui_QuestionsWidget

class QuestionsWidget(QtWidgets.QWidget, Ui_QuestionsWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_QuestionsWidget()
        self.ui.setupUi(self)

    def open(self, fileName):
        print('Opening...')