import pytest
from pytestqt.qtbot import QtBot


def test_main_view(qtbot:QtBot):
    from genial.views.mainview import MainView
    main_view = MainView()
    assert main_view is not None
    qtbot.add_widget(main_view)
    main_view.show()
    assert main_view.isVisible()


def test_document_view(qtbot:QtBot):
    from genial.views.documentview import DocumentView
    document_view = DocumentView()
    assert document_view is not None
    qtbot.add_widget(document_view)
    document_view.show()
    assert document_view.isVisible()


def test_properties_view(qtbot:QtBot):
    from genial.views.propertiesview import PropertiesView
    properties_view = PropertiesView()
    assert properties_view is not None
    qtbot.add_widget(properties_view)
    properties_view.show()
    assert properties_view.isVisible()


def test_questions_view(qtbot:QtBot):
    from genial.views.questionsview import QuestionsView
    questions_view = QuestionsView()
    assert questions_view is not None
    qtbot.add_widget(questions_view)
    questions_view.show()
    assert questions_view.isVisible()


def test_properties_questions_view(qtbot:QtBot):
    from genial.views.propertiesquestiontypeview import PropertiesQuestionTypeView
    properties_questions_view = PropertiesQuestionTypeView()
    assert properties_questions_view is not None
    qtbot.add_widget(properties_questions_view)
    properties_questions_view.show()
    assert properties_questions_view.isVisible()

