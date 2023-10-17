import pytest
from datetime import datetime

from utils.message_utils import convert_dialogflow_message, convertUserMessage


@pytest.mark.parametrize("dialogflowMessage, userNumber, expected_output", [
    ("Hello from Dialogflow", "1234567890",
     {'sender': "ChatBot", 'phoneNumber': "1234567890", 'body': "Hello from Dialogflow",
      "time": datetime.now().strftime("%H:%M")}),
    (None, "0987654321", {'sender': "ChatBot", 'phoneNumber': "0987654321", 'body': "Could not understand your message",
                          "time": datetime.now().strftime("%H:%M")}),
])
def test_convert_dialogflow_message(dialogflowMessage, userNumber, expected_output):
    output = convert_dialogflow_message(dialogflowMessage, userNumber)
    assert output == expected_output


@pytest.mark.parametrize("userMessage, expected_output", [
    ({"From": ["whatsapp:1234567890"], "ProfileName": ["JohnDoe"], "Body": ["Hello from WhatsApp"]},
     {'sender': "JohnDoe", 'from': "whatsapp", 'phoneNumber': "1234567890", 'body': "Hello from WhatsApp",
      "time": datetime.now().strftime("%H:%M")}),
    ({"From": ["instagram:0987654321"], "MediaUrl0": ["http://example.com/image.jpg"]},
     {'sender': "0987654321", 'from': "instagram", 'phoneNumber': "0987654321", 'body': "http://example.com/image.jpg",
      "time": datetime.now().strftime("%H:%M")}),
])
def test_convertUserMessage(userMessage, expected_output):
    output = convertUserMessage(userMessage)
    assert output == expected_output


if __name__ == '__main__':
    pytest.main()
