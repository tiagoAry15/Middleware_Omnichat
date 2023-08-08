import os
import datetime

from api_config.api_config import socketio
from socketEmissions.socket_emissor import pulseEmit
from utils.core_utils import processTwilioSandboxIncomingMessage
import requests


def processInstagramIncomingMessage(data):
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    message_text = data['entry'][0]['messaging'][0]['message']['text']
    structuredMessage = {'Body': [message_text], 'From': [f'whatsapp:+5585{sender_id}'], 'ProfileName': [sender_id]}
    mainResponse = processTwilioSandboxIncomingMessage(structuredMessage)
    txtResponse = mainResponse["body"]
    sendInstagramMessage(sender_id, txtResponse)
    currentFormattedTime = datetime.datetime.now().strftime("%H:%M")
    emitDict = {'body': message_text, 'from': 'instagram', 'phoneNumber': sender_id, 'sender': 'Mateus',
                'time': currentFormattedTime}
    # socketInstance.emit('message', emitDict)
    pulseEmit(socketio, emitDict)


def sendInstagramMessage(recipient_id, message_text):
    access_token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
    headers = {'Content-Type': 'application/json'}
    data = {'recipient': {'id': recipient_id}, 'message': {'text': message_text}}
    params = {'access_token': access_token}
    response = requests.post('https://graph.facebook.com/v13.0/me/messages', headers=headers, params=params, json=data)
    if response.status_code != 200:
        print(f"Unable to send message: {response.text}")
