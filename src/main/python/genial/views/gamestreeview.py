"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_gamestreeview import Ui_GamesTreeView


class GamesTreeView(QWidget, Ui_GamesTreeView):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_GamesTreeView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

from genial.resources import icons_rc
from genial.resources import locale_rc
