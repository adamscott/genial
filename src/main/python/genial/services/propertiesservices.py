"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject

from genial.views.propertiesview import PropertiesView

from genial.services.documentservice import document_service


class PropertiesService(QObject):
    window = None  # type: PropertiesView

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    def show(self, tab_wanted: str = 'general'):
        if self.window is None:
            self.window = PropertiesView()
            self.window.hide()
        if tab_wanted == 'question_types':
            self.window.set_tab('question_types')
        else:
            self.window.set_tab('general')
        self.window.exec()


properties_service = PropertiesService()

from genial.resources import icons_rc
from genial.resources import locale_rc
