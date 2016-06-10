"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QWidget, QMdiSubWindow
from PyQt5.QtCore import pyqtSignal

from genial.views.gen.ui_documentview import Ui_DocumentView


class DocumentView(QWidget, Ui_DocumentView):

    subwindows = None  # type: Dict[QWidget, QMdiSubWindow]

    document_available = pyqtSignal()
    document_unavailable = pyqtSignal()
    document_was_modified = pyqtSignal()
    document_open = pyqtSignal()
    document_close = pyqtSignal()
    document_requesting_settings_categories = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_DocumentView()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.subwindows = {}

    def add_window(self, widget: QWidget, tab_name: str = None):
        sub_window = QMdiSubWindow()
        sub_window.setWidget(widget)
        if tab_name is not None:
            sub_window.setWindowTitle(tab_name)
        self.subwindows[widget] = sub_window
        self.ui.mdi_area.addSubWindow(sub_window)
