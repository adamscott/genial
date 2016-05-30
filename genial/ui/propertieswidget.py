"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from genial.ui.ui_propertieswidget import Ui_PropertiesWidget

class PropertiesWidget(QtWidgets.QWidget, Ui_PropertiesWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_PropertiesWidget()
        self.ui.setupUi(self)