from datetime import datetime
import pytest

from unittest.mock import patch, Mock

from message_converter import MessageConverter


@pytest.fixture
def mock_datetime(monkeypatch):
    mock = Mock()
    mock_now = datetime(2021, 7, 14, 16, 0)
    mock.now.return_value = mock_now
    monkeypatch.setattr('message_converter.datetime', mock)
    return mock


@patch('omnichatTests.classes.message_converter.datetime')
def test_convert_user_message(mock_datetime):
    mock_now = datetime(2021, 7, 14, 16, 0)
    mock_datetime.now.return_value = mock_now
    user_message = {
        "Body": ["oi"],
        "From": ["whatsapp:+558599999999"],
        "ProfileName": ["Mateus"]
    }
    expected = {
        'sender': 'Mateus',
        'from': 'whatsapp',
        'phoneNumber': '+558599999999',
        'body': 'oi',
        "time": "2021-07-14 16:00"
    }
    result = MessageConverter.convert_user_message(user_message)

    assert result == expected, f"Erro: Esperado {expected}, mas obteve {result}"


@patch('omnichatTests.classes.message_converter.datetime')
def test_convert_dialogflow_message(mock_datetime):
    mock_now = datetime(2021, 7, 14, 16, 0)
    mock_datetime.now.return_value = mock_now
    dialogflow_message = {
        "query_result": {
            "fulfillment_text": "Olá, eu sou o chatbot da empresa X"
        }
    }
    expected = {
        'sender': 'ChatBot',
        'phoneNumber': '+558599999999',
        'body': {'query_result': {'fulfillment_text': 'Olá, eu sou o chatbot da empresa X'}},
        "time": "2021-07-14 16:00"
    }
    assert MessageConverter.convert_dialogflow_message(dialogflow_message, "+558599999999") == expected
