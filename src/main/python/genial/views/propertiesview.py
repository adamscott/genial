"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QDialog
from genial.views.gen.ui_propertiesview import Ui_PropertiesView


class PropertiesView(QDialog, Ui_PropertiesView):
    def __init__(self,parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_PropertiesView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_general_tab()
        self.setup_categories_tab()

    def setup_general_tab(self):
        pass

    def setup_categories_tab(self):
        pass

    def set_tab(self, tab_name):
        if tab_name == 'question_types':
            self.ui.tab_widget.setCurrentWidget(
                self.ui.question_types_tab
            )
        else:
            self.ui.tab_widget.setCurrentWidget(
                self.ui.general_tab
            )

    def show_question_types(self):
        self.ui.tab_widget.setCurrentWidget(self.ui.question_types_tab)

from genial.resources import icons_rc
from genial.resources import locale_rc
