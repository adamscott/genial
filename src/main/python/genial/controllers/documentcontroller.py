"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject
from genial.views.documentview import DocumentView
from genial.services.documentservice import DocumentService


class DocumentController(QObject):
    view = None  # type: DocumentView

    def start(self):
        if self.view is None:
            self.view = DocumentView()
            self.view.show()
        pass

    def request_new_document(self) -> bool:
        pass
