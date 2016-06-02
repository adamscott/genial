"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.ui.ui_categorywidget import Ui_CategoryWidget


class CategoryWidget(QWidget, Ui_CategoryWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_CategoryWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)