"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QObject, QCoreApplication, QDir, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlDriver, QSqlTableModel

from genial.ui.ui_documentwidget import Ui_DocumentWidget

from zipfile import ZipFile
from tempfile import TemporaryDirectory, TemporaryFile


class DocumentWidget(QWidget, Ui_DocumentWidget):
    document_available = pyqtSignal()
    document_unavailable = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_DocumentWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.file = None

    def open_file_name(self) -> str:
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker,PyArgumentList
        filter_genial_files = _translate('DocumentWidget', 'Génial files (*.gnl)')
        # noinspection PyTypeChecker,PyArgumentList
        filter_all_files = _translate('DocumentWidget', 'All files (*.*)')
        filters = [filter_genial_files, filter_all_files]
        filters_joined = ";;".join(filters)
        # noinspection PyTypeChecker,PyArgumentList
        file_name = QFileDialog.getOpenFileName(
            self,
            _translate('DocumentWidget', 'Open document…'),
            QDir.homePath(),
            filters_joined,
            filter_genial_files
        )
        return file_name

    def save_file_name(self) -> str:
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker,PyArgumentList
        filter_genial_files = _translate('DocumentWidget', 'Génial files (*.gnl)')
        # noinspection PyTypeChecker,PyArgumentList
        filter_all_files = _translate('DocumentWidget', 'All files (*.*)')
        filters = [filter_genial_files, filter_all_files]
        filters_joined = ";;".join(filters)
        # noinspection PyTypeChecker,PyArgumentList
        file_name = QFileDialog.getSaveFileName(
            self,
            _translate('DocumentWidget', 'Save document as…'),
            QDir.homePath(),
            filters_joined,
            filter_genial_files
        )
        return file_name

    def new_file(self):
        if self.file is not None:
            if not self.file.close():
                return
        self.file = DocumentFile(self)
        self.file.new()
        self.document_available.emit()

    def open_file(self):
        if self.file is not None:
            if not self.file.close():
                return

        file_name = self.open_file_name()

        self.file = DocumentFile(self)
        self.file.open(file_name)
        self.document_available.emit()

    def save_file(self):
        if self.file is not None:
            self.file.save()

    def save_file_as(self):
        if self.file is not None:
            self.file.save_as()

    def close_file(self) -> bool:
        if self.file is not None:
            if self.file.close():
                self.document_unavailable.emit()
                return True
            else:
                return False
        else:
            return True


class DocumentFile(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.document_widget = parent  # type: DocumentWidget
        self.directory = TemporaryDirectory()
        self.dirty = False  # type: bool
        self.database = None  # type: QSqlDatabase
        self.file_name = None  # type: str

    def new(self):
        self.dirty = False
        self.database = QSqlDatabase()
        self.database.addDatabase("QSQLITE", ":memory:")

    def open(self, file_name):
        _translate = QCoreApplication.translate
        try:
            with ZipFile(file_name) as z:
                pass
            pass
        except OSError as err:
            message_box = QMessageBox()
            message_box.critical(self.document_widget, "Génial", err.strerror)
        except (RuntimeError, NotImplementedError) as err:
            message_box = QMessageBox()
            # noinspection PyTypeChecker,PyArgumentList
            message_box.critical(
                self.document_widget,
                "Génial",
                _translate(
                    "DocumentWidget",
                    "Génial cannot open {}.".format(file_name)
                )
            )

    def save(self):
        if self.dirty:
            self.save_as(self.file_name)

    def save_as(self, file_name:str=None):
        if file_name is None:
            file_name = self.document_widget.save_file_name()
        cloned_database = QSqlDatabase.cloneDatabase(
            self.database,
            "{}/genial.db".format(self.directory)
        )  # type: QSqlDatabase

    def close(self) -> bool:
        _translate = QCoreApplication.translate
        if not self.dirty:
            self.cleanup()
            return True
        else:
            message_box = QMessageBox()

            # noinspection PyTypeChecker,PyArgumentList
            ret = message_box.warning(
                self.document_widget,
                _translate(
                    "DocumentWidget",
                    "Save document?"
                ),
                _translate(
                    "DocumentWidget",
                    "Changes will be lost if you don't save."
                ),
                buttons=QMessageBox.Discard | QMessageBox.Save | QMessageBox.Cancel,
                defaultButton=QMessageBox.Save
            )

            if ret == QMessageBox.Save:
                self.save()
            elif ret == QMessageBox.Cancel:
                return False
            else:
                self.cleanup()
                return True

    def cleanup(self):
        self.database.close()
        self.database = None
        self.directory.cleanup()
        self.database = None