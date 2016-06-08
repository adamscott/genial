"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QObject, QFile, QFileInfo, Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QUndoStack
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from typing import List, Dict


# noinspection PyArgumentList
class DocumentService(QObject):
    document = None  # type: Document

    document_created = pyqtSignal()
    document_closed = pyqtSignal()

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

    def initialize_document(self, path: str = None):
        self.document = Document(path)

    def new(self) -> bool:
        if self.document is None:
            self.initialize_document()
        else:
            if self.document.is_modified:
                pass
        self.document_created.emit()

    def open(self) -> bool:
        if self.document is None:
            _translate = QCoreApplication.translate
            # noinspection PyTypeChecker
            file_name = QFileDialog.getOpenFileName(
                caption=_translate("DocumentService", "Open File"),
                filter=";;".join(self.open_filters),
                initialFilter=self.open_initial_filter
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
                    return True
                elif result == QMessageBox.Discard:
                    self.document.dispose()
                    self.document = None
                    self.document_closed.emit()
                    return True
                else:  # result == QMessageBox.Cancel
                    return False
        return True

    def undo(self):
        pass

    def redo(self):
        pass

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


class Document(QObject):
    file = None  # type: QFile
    database = None  # type: QSqlDatabase

    question_type_model_instance = None  # type: QSqlTableModel

    def __init__(self, path: QFile = None):
        QObject.__init__(self)
        if path is None:
            self.new()
        else:
            self.open(path)

    def new(self):
        # noinspection PyTypeChecker,PyCallByClass
        self.database = QSqlDatabase.addDatabase('QSQLITE', ':memory:')
        self.init_database()

    def open(self, path: QFile = None):
        file_path = path.fileName()  # type: str
        zip_file = ZippedDocument.open(file_path)
        self.database = QSqlDatabase.cloneDatabase(
            zip_file.database,
            ':memory:'
        )
        self.init_database()
        zip_file.close()

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

        #query = QSqlQuery(self.database)
        #query_command = "INSERT INTO 'question_type' VALUES (null, 'Général', 0)"
        #if not query.exec(query_command):
        #    raise ConnectionError(query.lastError().text())

    def dispose(self):
        self.file = None
        if self.database:
            self.database.close()
        self.database = None

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


class ZippedDocument():
    zip_file = None  # type: ZipFile
    database = None  # type: QSqlDatabase

    @staticmethod
    def open(path: str) -> 'ZippedDocument':
        zipped_document = ZippedDocument()
        zipped_document.zip_file = ZipFile(path)
        zipped_document.read_database()
        return zipped_document

    def read_database(self):
        tmp_file = NamedTemporaryFile()  # type: NamedTemporaryFile
        with self.zip_file.open('genial.db') as zipped_db_buffer:
            with open(tmp_file.name) as tmp_file_buffer:
                tmp_file_buffer.write(zipped_db_buffer.read())
                tmp_file_buffer.close()
            zipped_db_buffer.close()
        self.database = QSqlDatabase()
        self.database.addDatabase('QSQLITE', tmp_file.name)

    def close(self):
        if self.database is not None:
            self.database.close()


document_service = DocumentService()  # type: DocumentService
