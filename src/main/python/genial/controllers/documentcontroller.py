"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject
from genial.views.documentview import DocumentView
from genial.models.documentmodel import DocumentModel


class DocumentController(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    def bind(self, view:DocumentView, model:DocumentModel):
        self.view = view
        self.model = model
        self.view.show()

    def start(self):
        pass