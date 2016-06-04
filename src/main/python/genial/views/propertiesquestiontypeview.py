"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_categoryview import Ui_CategoryView


class CategoryView(QWidget, Ui_CategoryView):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_CategoryView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)