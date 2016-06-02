"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale, Qt
from PyQt5.QtWidgets import QApplication

from genial.views.mainview import MainView
from genial.controllers.maincontroller import MainController
from genial.models.mainmodel import MainModel

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

    main_controller = MainController(app)
    main_controller.bind(MainView(), MainModel())
    main_controller.start()

    return app.exec_()

