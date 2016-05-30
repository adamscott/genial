"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QApplication

from genial.mainwindow import MainWindow


def run():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

