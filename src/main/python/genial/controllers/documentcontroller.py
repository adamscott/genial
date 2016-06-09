"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject, pyqtSlot
from genial.views.documentview import DocumentView
from genial.services import document_service
from genial.controllers.questionscontroller import QuestionsController
from genial.views.questionsview import QuestionsView


class DocumentController(QObject):
    view = None  # type: DocumentView
    questions_controller = None  # type: QuestionsController

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

    def open_questions(self):
        if self.questions_controller is None:
            from PyQt5.QtCore import QCoreApplication
            _translate = QCoreApplication.translate
            self.questions_controller = QuestionsController(self)
            self.questions_controller.view = QuestionsView(self.view)
            # noinspection PyTypeChecker, PyArgumentList
            self.view.add_window(
                self.questions_controller.view,
                _translate("DocumentController", "Questions")
            )
            self.questions_controller.start()

    @pyqtSlot()
    def on_document_created(self):
        self.open_questions()
        pass

    @pyqtSlot()
    def on_document_closed(self):
        pass
