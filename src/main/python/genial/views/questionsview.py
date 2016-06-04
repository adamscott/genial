"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_questionsview import Ui_QuestionsView


class QuestionsView(QWidget, Ui_QuestionsView):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_QuestionsView()
        self.ui.setupUi(self)

    def open(self, filename):
        print('Opening...')