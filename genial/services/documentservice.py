"""

"""
from zipfile import ZipFile, BadZipFile, LargeZipFile
from tempfile import mkdtemp, NamedTemporaryFile
from typing import List, Dict, Union, Optional
import os
import shutil

from PyQt5.QtCore import QCoreApplication, QObject, QFile, QFileInfo, \
    pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QUndoStack
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlError

from genial.utils import logger
from genial import application


class DocumentError(Exception):
    original_error = None  # type: Exception
    message = None  # type: str

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error


class SqlError(Exception):
    original_error = None  # type: Exception
    message = None  # type: str

    def __init__(self, original_error: QSqlError = None):
        self.original_error = original_error
        self.message = self.original_error.text()


# noinspection PyArgumentList
class DocumentService(QObject):
    document = None  # type: Document

    document_created = pyqtSignal()
    document_closed = pyqtSignal()
    document_about_to_close = pyqtSignal()

    open_initial_filter = None  # type: str
    open_filters = None  # type: List[str]

    undo_stack = None  # type: QUndoStack

    def __init__(self):
        QObject.__init__(self)
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker
        self.open_initial_filter = _translate(
            "DocumentService",
            "Génial files (*.gnl)"
        )
        # noinspection PyTypeChecker
        self.open_filters = [
            self.open_initial_filter,
            _translate("DocumentService", "All files (*.*)")
        ]
        self.undo_stack = QUndoStack()
        self.connect_slots()

    @property
    def document_plugin_directory(self) -> Optional[str]:
        if self.document is not None:
            plugin_dir = "{}/plugins".format(self.document.tmp_directory)
            os.makedirs(plugin_dir, exist_ok=True)
            return plugin_dir
        else:
            return None

    @property
    def is_loaded(self) -> bool:
        return self.document is not None

    @property
    def question_types(self) -> List[str]:
        if self.document is not None:
            return self.document.question_types
        else:
            return []

    @property
    def question_type_model(self) -> QSqlTableModel:
        return self.document.question_type_model

    @property
    def properties(self) -> Dict[str, str]:
        if self.document is not None:
            return self.document.properties
        else:
            return []

    @property
    def database(self) -> QSqlDatabase:
        if self.document is not None:
            if self.document.database is not None:
                return self.document.database
        return None

    def connect_slots(self):
        application.app.aboutToQuit.connect(
            self.dispose
        )

    def connect_document_slots(self):
        self.document.error_occurred.connect(
            self.handle_document_error
        )
        self.document.document_created.connect(
            self.declare_document_as_created
        )
        self.document.document_disposed.connect(
            self.declare_document_as_closed
        )

    @pyqtSlot()
    def dispose(self):
        pass

    def initialize_document(self, path: str = None):
        self.document = Document()
        self.connect_document_slots()
        if path is not None:
            self.document.open(path)
        else:
            self.document.new()

    def new(self) -> bool:
        if self.document is None or not self.document.is_modified:
            self.initialize_document()
            return True
        else:
            if self.document.close():
                return self.new()
            else:
                return False

    def open(self) -> bool:
        if self.document is None:
            _translate = QCoreApplication.translate
            # noinspection PyTypeChecker
            file_name = QFileDialog.getOpenFileName(
                caption=_translate("DocumentService", "Open File"),
                filter=";;".join(self.open_filters),
                initialFilter=self.open_initial_filter,
                directory=os.path.expanduser("~")
            )
            if file_name[0] != '':
                self.initialize_document(file_name[0])
        else:
            self.close()

    def close(self) -> bool:
        if self.document is not None:
            if self.document.is_modified:
                _translate = QCoreApplication.translate
                message_box = QMessageBox()
                # noinspection PyTypeChecker
                save_document = _translate(
                    "DocumentService",
                    "Save document \"{}\"?".format(self.document.name)
                )
                # noinspection PyTypeChecker
                document_modified = _translate(
                    "DocumentService",
                    "The document has been modified."
                )
                # noinspection PyTypeChecker
                save_changes = _translate(
                    "DocumentService",
                    "Do you want to save your changes?"
                )
                message_box.setWindowTitle(save_document)
                message_box.setText(document_modified)
                message_box.setInformativeText(save_changes)
                message_box.setStandardButtons(
                    QMessageBox.Save |
                    QMessageBox.Discard |
                    QMessageBox.Cancel
                )
                result = message_box.exec()
                if result == QMessageBox.Save:
                    self.save()
                elif result == QMessageBox.Cancel:
                    return False
            # The document is disposed for files not modified, saved and discarded
            self.document_about_to_close.emit()
            self.document.dispose()
        return True

    def undo(self):
        pass

    def redo(self):
        pass

    @pyqtSlot(DocumentError)
    def handle_document_error(self, e: DocumentError):
        _translate = QCoreApplication.translate
        # noinspection PyTypeChecker
        an_error_occurred = _translate("DocumentService", "An error occurred.")
        # noinspection PyTypeChecker
        an_error_occurred_detail = _translate(
            "DocumentService",
            "An error occurred while handling the document."
        )
        message_box = QMessageBox()
        if self.document.path is not None:
            message_box.setWindowFilePath(self.document.path)
        else:
            message_box.setWindowTitle(an_error_occurred)
        message_box.setText(an_error_occurred_detail)
        message_box.setInformativeText(e.message)
        logger.error(e)
        message_box.exec()
        self.document = None

    @pyqtSlot()
    def declare_document_as_created(self):
        self.document_created.emit()

    @pyqtSlot()
    def declare_document_as_closed(self):
        self.document = None
        self.document_closed.emit()


class Document(QObject):
    file = None  # type: QFile
    database = None  # type: QSqlDatabase
    tmp_directory = None  # type: str

    error_occurred = pyqtSignal(DocumentError)
    document_created = pyqtSignal()
    document_disposed = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.init_tmp_directory()

    @property
    def path(self) -> str:
        if self.file is None:
            return self.name
        else:
            return self.file.fileName()

    @property
    def name(self) -> str:
        _translate = QCoreApplication.translate
        if self.file is not None:
            return QFileInfo(self.file.fileName()).fileName()
        else:
            # noinspection PyArgumentList, PyTypeChecker
            return _translate("DocumentService", "Untitled")
        pass

    pass

    @property
    def question_types(self) -> List[str]:
        question_type_list = []  # type: List[str]
        query_command = "SELECT * FROM 'question_type'"
        query = QSqlQuery(self.database)
        if not query.exec(query_command):
            raise ConnectionError(query.lastError().text())
        question_type_field_id = query.record().indexOf('name')
        while query.next():
            question_type_list.append(
                query.value(question_type_field_id)
            )
        return question_type_list

    @property
    def properties(self) -> Dict[str, str]:
        return {}

    @property
    def is_modified(self) -> bool:
        return False

    def new(self):
        self.init_tmp_directory()
        # noinspection PyTypeChecker,PyCallByClass
        self.database = QSqlDatabase.addDatabase('QSQLITE', ':memory:')
        self.init_database()
        self.document_created.emit()

    def open(self, path: str):
        _translate = QCoreApplication.translate
        self.file = QFile(path)
        if self.file.exists():
            file_path = self.file.fileName()  # type: str
            open_gnl_file_result = self.open_gnl_file(file_path, self.tmp_directory)
            logger.debug(open_gnl_file_result)
            logger.debug(isinstance(open_gnl_file_result, ZippedDocument))
            if isinstance(open_gnl_file_result, ZippedDocument):
                zip_file = open_gnl_file_result  # type: ZipFile
                # noinspection PyTypeChecker,PyCallByClass
                self.database = QSqlDatabase.cloneDatabase(
                    zip_file.database,
                    ':memory:'
                )
                self.init_database()
                zip_file.close()
                self.document_created.emit()
            else:
                self.error_occurred.emit(open_gnl_file_result)
        else:
            self.file = None
            selected_file_does_not_exist = _translate(
                "DocumentService",
                "The selected file ({}) does not exist."
            )
            self.error_occurred.emit(
                DocumentError(
                    selected_file_does_not_exist.format(
                        path
                    )
                )
            )

    def init_database(self):
        success = self.database.open()

        if not success:
            raise ConnectionError(self.database.lastError().text())

        query = QSqlQuery(self.database)
        query_command = "CREATE TABLE IF NOT EXISTS 'question_type' ({}{}{})".format(
            'id integer primary key,',
            'name text,',
            'position integer'
        )
        if not query.exec(query_command):
            raise ConnectionError(query.lastError().text())

    def init_tmp_directory(self):
        self.tmp_directory = mkdtemp()

    def dispose(self):
        self.file = None
        if self.database:
            self.database.close()
        self.database = None
        shutil.rmtree(self.tmp_directory)
        self.document_disposed.emit()

    @staticmethod
    def open_gnl_file(file_path: str, tmp_directory: str) -> Union['ZippedDocument', DocumentError]:
        _translate = QCoreApplication.translate
        output = None  # type: Union[ZippedDocument, DocumentError]
        try:
            zip_file = ZippedDocument.open(file_path, tmp_directory)
            output = zip_file
        except BadZipFile as e:
            # noinspection PyArgumentList, PyTypeChecker
            file_not_valid = _translate(
                "DocumentService",
                "The file ({}) is not a valid .gnl file."
            )
            output = DocumentError(
                file_not_valid.format(
                    file_path
                ),
                e
            )
        except LargeZipFile as e:
            # noinspection PyArgumentList, PyTypeChecker
            file_too_big = _translate(
                "DocumentService",
                "The file ({}) is too big."
            )
            output = DocumentError(
                file_too_big.format(
                    file_path
                ),
                e
            )
        except SqlError as e:
            # noinspection PyArgumentList, PyTypeChecker
            database_corrupted = _translate(
                "DocumentService",
                "The internal database of the file ({}) is corrupted."
            )
            output = DocumentError(
                database_corrupted.format(
                    file_path
                ),
                e
            )
        except Exception as e:
            # noinspection PyArgumentList, PyTypeChecker
            unhandled_error = _translate(
                "DocumentService",
                "An unhandled error."
            )
            output = DocumentError(
                unhandled_error,
                e
            )
        finally:
            assert isinstance(output, ZippedDocument) or isinstance(output, DocumentError)
            return output


class ZippedDocument (QObject):
    zip_file = None  # type: ZipFile
    database = None  # type: QSqlDatabase
    plugins = None  # type: str

    @staticmethod
    def open(path: str, tmp_directory: str) -> 'ZippedDocument':
        zipped_document = ZippedDocument()
        zipped_document.zip_file = ZipFile(path)
        zipped_document.extract(tmp_directory)
        return zipped_document

    def extract(self, tmp_directory: str):
        for file in self.zip_file.namelist():
            target_path = "{}/{}".format(tmp_directory, file)
            logger.debug('Extracting {} to "{}"'.format(file, target_path))
            self.zip_file.extract(file, path=tmp_directory)
            if file == 'genial.db':
                self.read_database(target_path)

    def read_database(self, file_name: str):
        # noinspection PyTypeChecker,PyCallByClass
        self.database = QSqlDatabase.addDatabase('QSQLITE', file_name)
        if self.database.lastError().type() != QSqlError.NoError:
            raise SqlError(
                self.database.lastError()
            )

    def close(self):
        if self.database is not None:
            self.database.close()
