"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.ui.ui_questionswidget import Ui_QuestionsWidget


class QuestionsWidget(QWidget, Ui_QuestionsWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_QuestionsWidget()
        self.ui.setupUi(self)

    def open(self, filename):
        print('Opening...')