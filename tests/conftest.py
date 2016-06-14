import os
import pytest


@pytest.yield_fixture(scope="session")
def app():
    from genial import application
    yield application.app
    application.app.quit()