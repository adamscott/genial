"""

"""
from PyQt5.QtCore import QObject, pyqtSlot
from genial.views.questionsview import QuestionsView
from genial.services import document_service
from genial.services import properties_service


class QuestionsController(QObject):
    view = None  # type: QuestionsView

    def start(self):
        if self.view is None:
            self.view = QuestionsView()
        self.setup_view()
        self.view.show()
        self.connect_slots()

    def setup_view(self):
        if len(document_service.question_types) > 0:
            self.view.set_has_type()
        else:
            self.view.set_no_type()

    def connect_slots(self):
        self.view.properties_button_triggered.connect(
            self.on_properties_button_triggered
        )

    @pyqtSlot()
    def on_properties_button_triggered(self):
        properties_service.show('question_types')
