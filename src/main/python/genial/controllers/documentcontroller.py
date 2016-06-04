"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject, pyqtSlot
from genial.views.documentview import DocumentView
from genial.services.documentservice import document_service


class DocumentController(QObject):
    view = None  # type: DocumentView

    def start(self):
        if self.view is None:
            self.view = DocumentView()
            self.view.show()
        self.connect_slots()

    def connect_slots(self):
        document_service.document_created.connect(
            self.on_document_created
        )
        document_service.document_closed.connect(
            self.on_document_closed
        )

    @pyqtSlot()
    def on_document_created(self):
        if len(document_service.categories) > 0:
            self.view.show_main()
        else:
            self.view.show_no_question_type()

    @pyqtSlot()
    def on_document_closed(self):
        self.view.show_no_document()
