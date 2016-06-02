"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject
from genial.views.mainview import MainView
from genial.models.mainmodel import MainModel


class MainController(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    def bind(self, view:MainView, model:MainModel):
        self.view = view
        self.model = model
        self.view.show()

    def start(self):
        pass