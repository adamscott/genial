"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget
from genial.views.gen.ui_propertiesview import Ui_PropertiesView


class PropertiesView(QWidget, Ui_PropertiesView):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_PropertiesView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_general_tab()
        self.setup_categories_tab()

    def setup_general_tab(self):
        pass

    def setup_categories_tab(self):
        pass