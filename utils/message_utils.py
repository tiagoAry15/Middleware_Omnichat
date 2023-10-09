from datetime import datetime


def convert_dialogflow_message(dialogflowMessage, userNumber):
    return {
        'sender': "ChatBot",
        'phoneNumber': userNumber,
        'body': dialogflowMessage if dialogflowMessage is not None else "Could not understand your message",
        "time": datetime.now().strftime("%H:%M"),
    }


def convertUserMessage(userMessage: dict) -> dict:
    social_network, userNumber = userMessage['From'][0].split(":")
    sender = userMessage['ProfileName'][0] if social_network == "whatsapp" else userNumber
    receivedMessage = userMessage['Body'][0] if 'Body' in userMessage else userMessage['MediaUrl0'][0]

    return {
        'sender': sender,
        'from': social_network,
        'phoneNumber': userNumber,
        'body': receivedMessage,
        "time": datetime.now().strftime("%H:%M"),
    }