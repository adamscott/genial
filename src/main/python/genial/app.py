"""
    Génial
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
import sys

from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication


def run():
    global app

    # Imports .qrc resources even if it is "unused"
    from genial.resources import icons_rc
    from genial.resources import locale_rc
    from genial.resources import plugins_rc

    # Initializes the app variable
    app = QApplication(sys.argv)
    app.setApplicationName("Génial")
    app.setApplicationDisplayName("Génial")
    app.setProperty("AA_EnableHighDpiScaling", True)
    # Importing here makes available PyQt5.QtWidgets.QApplication.instance()
    # for each of these modules (and for their imports too.)
    from genial.controllers.maincontroller import MainController

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

    app.exec()


app = None  # type: QApplication
