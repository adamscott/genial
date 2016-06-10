"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_questionsview import Ui_QuestionsView


class QuestionsView(QWidget, Ui_QuestionsView):
    properties_button_triggered = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_QuestionsView()
        self.ui.setupUi(self)

    def set_no_type(self):
        self.ui.stacked_widget.setCurrentWidget(
            self.ui.no_type
        )

    def set_has_type(self):
        self.ui.stacked_widget.setCurrentWidget(
            self.ui.has_type
        )

    @pyqtSlot()
    def on_properties_button_clicked(self):
        self.properties_button_triggered.emit()
