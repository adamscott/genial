"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale, Qt
from PyQt5.QtWidgets import QApplication

from genial.mainwindow import MainWindow


def run():
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("Génial")
    app.setApplicationDisplayName("Génial")
    app.setProperty("AA_EnableHighDpiScaling", True)
    translator = QTranslator()
    if translator.load(QLocale(), "genial", "_", ":/locale"):
        # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
        QCoreApplication.installTranslator(translator)
    window = MainWindow()
    window.show()
    return app.exec_()

