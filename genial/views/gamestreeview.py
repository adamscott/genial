"""

"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_gamestreeview import Ui_GamesTreeView


class GamesTreeView(QWidget, Ui_GamesTreeView):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_GamesTreeView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
