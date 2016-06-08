"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import Qt, QObject, QSortFilterProxyModel
from PyQt5.QtSql import QSqlTableModel

from genial.controllers.propertiescontroller import PropertiesController

from genial.services.documentservice import document_service


class PropertiesService(QObject):
    controller = None  # type: PropertiesController
    question_type_model = None  # type: QSqlTableModel
    question_type_filter_proxy_model = None  # type: 'QuestionTypeFilterProxyModel'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    def show(self, tab_wanted: str = 'general'):
        if document_service.database is not None:
            if self.question_type_model is None:
                self.question_type_model = QSqlTableModel(
                    self,
                    document_service.database
                )
                self.question_type_model.setTable("question_type")
                self.question_type_model.setEditStrategy(
                    QSqlTableModel.OnManualSubmit
                )
                self.question_type_filter_proxy_model = QuestionTypeFilterProxyModel()
                self.question_type_filter_proxy_model.setSourceModel(
                    self.question_type_model
                )
                self.question_type_filter_proxy_model.sort(
                    self.question_type_model.fieldIndex("position"),
                    Qt.AscendingOrder
                )
                self.question_type_filter_proxy_model.setDynamicSortFilter(True)

        if self.controller is None:
            self.controller = PropertiesController()
            self.controller.start()
        self.controller.show(tab_wanted)


class QuestionTypeFilterProxyModel (QSortFilterProxyModel):
    pass

properties_service = PropertiesService()
