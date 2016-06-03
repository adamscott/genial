"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import QApplication

from genial.controllers.maincontroller import MainController


def run():
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Génial")
    app.setApplicationDisplayName("Génial")
    app.setProperty("AA_EnableHighDpiScaling", True)

    # Qt translation
    qt_translator = QTranslator()
    if qt_translator.load(QLocale(), "qt", "_", ":/locale"):
        # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
        QCoreApplication.installTranslator(qt_translator)

    # App translation
    genial_translator = QTranslator()
    if genial_translator.load(QLocale(), "genial", "_", ":/locale"):
        # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
        QCoreApplication.installTranslator(genial_translator)

    main_controller = MainController(app)
    main_controller.start()

    return app.exec()
