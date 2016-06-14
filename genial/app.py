"""

"""
import sys

from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication


class Application:
    _app = None  # type: QApplication

    @property
    def app(self) -> QApplication:
        if self._app is None:
            self.setup()
        return self._app

    def setup(self) -> None:
        # Imports .qrc resources even if it is "unused"
        from genial.resources import icons_rc
        from genial.resources import locale_rc
        from genial.resources import plugins_rc

        # Initializes the app variable
        self._app = QApplication(sys.argv)
        self._app.setApplicationName("Génial")
        self._app.setApplicationDisplayName("Génial")
        self._app.setProperty("AA_EnableHighDpiScaling", True)

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

    def run(self) -> int:
        # Importing here makes available PyQt5.QtWidgets.QApplication.instance()
        # for each of these modules (and for their imports too.)
        from genial.controllers.maincontroller import MainController
        main_controller = MainController(self.app)
        main_controller.start()
        return self.app.exec()

