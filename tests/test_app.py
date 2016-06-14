from PyQt5.QtWidgets import QApplication
import pytest


def test_application_name(app: QApplication):
    assert app is not None
    assert app.applicationName() == "Génial"


def test_application_display_name(app: QApplication):
    assert app is not None
    assert app.applicationDisplayName() == "Génial"


def test_application_has_high_dpi_scaling(app:QApplication):
    assert app is not None
    assert app.property("AA_EnableHighDpiScaling") == True
