"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QStackedWidget
from PyQt5.QtCore import QObject, QCoreApplication, QDir, pyqtSignal, pyqtSlot
from PyQt5.QtSql import QSqlDatabase, QSqlDriver, QSqlTableModel

from genial.views.gen.ui_documentview import Ui_DocumentView

from zipfile import ZipFile
from tempfile import TemporaryDirectory, TemporaryFile


class DocumentView(QWidget, Ui_DocumentView):
    document_available = pyqtSignal()
    document_unavailable = pyqtSignal()
    document_was_modified = pyqtSignal()
    document_open = pyqtSignal()
    document_close = pyqtSignal()
    document_requesting_settings_categories = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_DocumentView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.file = None

    def show_no_document(self):
        stacked_widget = self.ui.stacked_widget  # type: QStackedWidget
        stacked_widget.setCurrentWidget(self.ui.no_document_page)

    def show_main(self):
        stacked_widget = self.ui.stacked_widget  # type: QStackedWidget
        stacked_widget.setCurrentWidget(self.ui.main_page)

    def show_no_question_type(self):
        stacked_widget = self.ui.stacked_widget  # type: QStackedWidget
        stacked_widget.setCurrentWidget(self.ui.no_question_type_page)
