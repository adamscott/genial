"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_gamestreewidget import Ui_GamesTreeWidget


class GamesTreeWidget(QWidget, Ui_GamesTreeWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_GamesTreeWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)