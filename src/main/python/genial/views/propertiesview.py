"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlTableModel
from genial.views.gen.ui_propertiesview import Ui_PropertiesView


class PropertiesView(QDialog, Ui_PropertiesView):

    button_ok_clicked = pyqtSignal()
    button_cancel_clicked = pyqtSignal()
    button_apply_clicked = pyqtSignal()

    button_add_question_type_clicked = pyqtSignal()
    button_remove_question_type_clicked = pyqtSignal()
    button_move_up_question_type_clicked = pyqtSignal()
    button_move_down_question_type_clicked = pyqtSignal()

    question_type_list_view_current_changed = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_PropertiesView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.set_icons()
        self.setup_general_tab()
        self.setup_categories_tab()
        self.connect_slots()

    # noinspection PyCallByClass,PyTypeChecker
    def set_icons(self):
        self.ui.add_question_type_button.setIcon(
            QIcon.fromTheme(
                'list-add',
                QIcon(':/icons/list-add.svg')
            )
        )
        self.ui.remove_question_type_button.setIcon(
            QIcon.fromTheme(
                'list-remove',
                QIcon(':/icons/list-remove.svg')
            )
        )
        self.ui.move_up_question_type_button.setIcon(
            QIcon.fromTheme(
                'go-up',
                QIcon(':/icons/go-up.svg')
            )
        )
        self.ui.move_down_question_type_button.setIcon(
            QIcon.fromTheme(
                'go-down',
                QIcon(':/icons/go-down.svg')
            )
        )

    def setup_general_tab(self):
        pass

    def setup_categories_tab(self):
        pass

    def connect_slots(self):
        self.ui.button_box.button(QDialogButtonBox.Ok).clicked.connect(
            self.on_button_box_button_ok_clicked
        )
        self.ui.button_box.button(QDialogButtonBox.Cancel).clicked.connect(
            self.on_button_box_button_cancel_clicked
        )
        self.ui.button_box.button(QDialogButtonBox.Apply).clicked.connect(
            self.on_button_box_button_apply_clicked
        )

    def connect_question_type_selected(self):
        if self.ui.question_type_list_view.selectionModel():
            self.ui.question_type_list_view.selectionModel().currentChanged.connect(
                self.on_question_type_list_view_current_changed
            )

    def set_tab(self, tab_name):
        if tab_name == 'question_type':
            self.ui.tab_widget.setCurrentWidget(
                self.ui.question_type_tab
            )
        else:
            self.ui.tab_widget.setCurrentWidget(
                self.ui.general_tab
            )

    def show_question_type(self):
        self.ui.tab_widget.setCurrentWidget(self.ui.question_type_tab)

    def set_model(self, model: QSqlTableModel, column: int):
        self.ui.question_type_list_view.setModel(model)
        self.ui.question_type_list_view.setModelColumn(column)
        self.connect_question_type_selected()

    def update_question_type_tools(self, current: QModelIndex = None):
        if current is not None:
            self.ui.remove_question_type_button.setDisabled(False)

            top_index = current.sibling(current.row() - 1, current.column())
            bottom_index = current.sibling(current.row() + 1, current.column())
            self.ui.move_up_question_type_button.setDisabled(not top_index.isValid())
            self.ui.move_down_question_type_button.setDisabled(not bottom_index.isValid())
        else:
            self.ui.remove_question_type_button.setDisabled(True)
            self.ui.move_up_question_type_button.setDisabled(True)
            self.ui.move_down_question_type_button.setDisabled(True)

    @property
    def selected_question_type(self) -> QModelIndex:
        return self.ui.question_type_list_view.currentIndex()

    @selected_question_type.setter
    def selected_question_type(self, index: QModelIndex = None):
        self.ui.question_type_list_view.setCurrentIndex(index)
        self.update_question_type_tools(index)

    @pyqtSlot(QModelIndex, QModelIndex)
    def on_question_type_list_view_current_changed(self,
                                                     current: QModelIndex,
                                                     previous: QModelIndex):
        self.update_question_type_tools(current)
        self.question_type_list_view_current_changed.emit(current, previous)

    @pyqtSlot()
    def on_add_question_type_button_clicked(self):
        self.button_add_question_type_clicked.emit()

    @pyqtSlot()
    def on_remove_question_type_button_clicked(self):
        self.button_remove_question_type_clicked.emit()

    @pyqtSlot()
    def on_move_up_question_type_button_clicked(self):
        self.button_move_up_question_type_clicked.emit()

    @pyqtSlot()
    def on_move_down_question_type_button_clicked(self):
        self.button_move_down_question_type_clicked.emit()

    @pyqtSlot()
    def on_button_box_button_ok_clicked(self):
        self.button_ok_clicked.emit()

    @pyqtSlot()
    def on_button_box_button_cancel_clicked(self):
        self.button_cancel_clicked.emit()

    @pyqtSlot()
    def on_button_box_button_apply_clicked(self):
        self.button_apply_clicked.emit()
