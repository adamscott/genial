"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject
from PyQt5.QtSql import QSqlDatabase


class DocumentService(QObject):
    database = None  # type: QSqlDatabase

    @property
    def is_loaded(self):
        return database is not None

