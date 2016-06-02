"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QObject

class MainModel(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
