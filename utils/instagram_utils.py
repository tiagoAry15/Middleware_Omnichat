import os
import datetime

from api_config.api_config import socketio
from socketEmissions.socket_emissor import pulseEmit
from utils.core_utils import updateFirebaseWithUserMessage, processDialogFlowMessage
import requests


def convertIncomingInstagramMessageToProperFormat(data):
    messageContent = data['entry'][0]['messaging'][0]['message']['text']
    senderId = data['entry'][0]['messaging'][0]['sender']['id']
    recipientId = data['entry'][0]['messaging'][0]['recipient']['id']
    incomingPlatform = data['object']
    toTag = f"{incomingPlatform}:{recipientId}"
    fromTag = f"{incomingPlatform}:{senderId}"
    return {"ProfileName": ["User"], "WaId": [senderId], "Body": [messageContent],
            "To": [toTag], "From": [fromTag], "senderId": senderId, "recipientId": recipientId,
            "Sender": senderId}


def processInstagramIncomingMessage(data: dict):
    sender_id = data["senderId"]
    userMessageJSON, chatData = updateFirebaseWithUserMessage(data)
    dialogflowMessageJSON = processDialogFlowMessage(userMessageJSON)
    response_body = dialogflowMessageJSON["body"]
    sendInstagramMessage(sender_id, response_body)


def sendInstagramMessage(recipient_id, message_text):
    access_token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
    headers = {'Content-Type': 'application/json'}
    data = {'recipient': {'id': recipient_id}, 'message': {'text': message_text}}
    params = {'access_token': access_token}
    response = requests.post('https://graph.facebook.com/v13.0/me/messages', headers=headers, params=params, json=data)
    if response.status_code != 200:
        print(f"Unable to send message: {response.text}")
