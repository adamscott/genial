"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject, QModelIndex, pyqtSlot

from genial.views.propertiesview import PropertiesView


class PropertiesController(QObject):
    view = None  # type: PropertiesView

    def start(self):
        from genial.services import properties_service
        if self.view is None:
            self.view = PropertiesView()
            self.view.set_model(
                properties_service.question_type_filter_proxy_model,
                properties_service.question_type_model.fieldIndex("name")
            )
            self.view.update_question_type_tools()
            self.connect_slots()

    def connect_slots(self):
        self.view.button_add_question_type_clicked.connect(
            self.on_button_add_question_type_clicked
        )
        self.view.button_remove_question_type_clicked.connect(
            self.on_button_remove_question_type_clicked
        )
        self.view.button_move_up_question_type_clicked.connect(
            self.on_button_move_up_question_type_clicked
        )
        self.view.button_move_down_question_type_clicked.connect(
            self.on_button_move_down_question_type_clicked
        )
        self.view.question_type_list_view_current_changed.connect(
            self.on_question_type_list_view_current_changed
        )
        self.view.button_ok_clicked.connect(
            self.on_button_ok_clicked
        )
        self.view.button_apply_clicked.connect(
            self.on_button_apply_clicked
        )
        self.view.button_cancel_clicked.connect(
            self.on_button_cancel_clicked
        )

    def apply_changes(self):
        from genial.services import properties_service
        properties_service.question_type_model.submitAll()

    def show(self, tab_wanted: str):
        from genial.services import properties_service
        properties_service.question_type_model.select()
        self.view.selected_question_type = properties_service.question_type_filter_proxy_model.index(
            0,
            properties_service.question_type_model.fieldIndex("name")
        )
        self.view.set_tab(tab_wanted)
        self.view.show()

    def hide(self):
        self.view.hide()

    def add_question_type(self):
        from genial.services import properties_service
        from PyQt5.QtCore import QCoreApplication
        _translate = QCoreApplication.translate

        # noinspection PyTypeChecker,PyArgumentList
        new_type_name = self.get_new_type_name(
            _translate("PropertiesController", "Default")
        )
        record = properties_service.question_type_model.record()
        record.setValue('name', new_type_name)
        row_count = properties_service.question_type_model.rowCount()
        record.setValue(
            'position',
            row_count
        )
        properties_service.question_type_model.insertRecord(
            row_count,
            record
        )
        self.view.selected_question_type = properties_service.question_type_filter_proxy_model.mapFromSource(
            properties_service.question_type_model.index(
                row_count,
                properties_service.question_type_model.fieldIndex("name")
            )
        )

    def move_selected_question_type(self, direction: str):
        from genial.services import properties_service
        current_name_index = self.view.selected_question_type
        current_position_index = current_name_index.sibling(
            current_name_index.row(),
            properties_service.question_type_model.fieldIndex("position")
        )
        # Switch with the next question type
        if direction == 'up':
            target_position_index = current_position_index.sibling(
                current_position_index.row() - 1,
                current_position_index.column()
            )
        elif direction == 'down':
            target_position_index = current_position_index.sibling(
                current_position_index.row() + 1,
                current_position_index.column()
            )
        else:
            return
        if target_position_index.isValid():
            mapped_current_position_index = properties_service.question_type_filter_proxy_model.mapToSource(
                current_position_index
            )
            mapped_target_position_index = properties_service.question_type_filter_proxy_model.mapToSource(
                target_position_index
            )
            current_record = properties_service.question_type_model.record(
                mapped_current_position_index.row()
            )
            target_record = properties_service.question_type_model.record(
                mapped_target_position_index.row()
            )
            properties_service.question_type_model.setData(
                mapped_current_position_index,
                target_record.value('position')
            )
            properties_service.question_type_model.setData(
                mapped_target_position_index,
                current_record.value('position')
            )
            self.view.selected_question_type = properties_service.question_type_filter_proxy_model.mapFromSource(
                mapped_current_position_index.sibling(
                    mapped_current_position_index.row(),
                    properties_service.question_type_model.fieldIndex("name")
                )
            )


    @staticmethod
    def get_new_type_name(name: str) -> str:
        from genial.services import properties_service
        if properties_service.question_type_model.rowCount() == 0:
            # There's no row. No need to check.
            return name
        name += "{}"
        name_i = 0
        final_name = ""
        while True:
            found_default = False
            for i in range(0, properties_service.question_type_model.rowCount()):
                row_record = properties_service.question_type_model.record(i)
                row_name = row_record.value("name")

                if name_i == 0:
                    final_name = name.format("")
                else:
                    final_name = name.format(name_i)

                if final_name == row_name:
                    found_default = True
                    break
            if not found_default:
                break
            else:
                name_i += 1
        return final_name

    @pyqtSlot(QModelIndex, QModelIndex)
    def on_question_type_list_view_current_changed(self,
                                                   current: QModelIndex,
                                                   previous: QModelIndex):
        if current is not None:
            pass

    @pyqtSlot()
    def on_button_add_question_type_clicked(self):
        self.add_question_type()

    @pyqtSlot()
    def on_button_remove_question_type_clicked(self):
        print('remove question type clicked')

    @pyqtSlot()
    def on_button_move_up_question_type_clicked(self):
        self.move_selected_question_type('up')

    @pyqtSlot()
    def on_button_move_down_question_type_clicked(self):
        self.move_selected_question_type('down')

    @pyqtSlot()
    def on_button_ok_clicked(self):
        self.apply_changes()
        self.hide()

    @pyqtSlot()
    def on_button_apply_clicked(self):
        self.apply_changes()

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.hide()
