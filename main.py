import json
import os

from dotenv import load_dotenv
from flask import Flask, request
import google.cloud.dialogflow_v2 as dialogflow
from google.cloud import dialogflow_v2beta1
from twilio.rest import Client

from analyzePizzaIntent import structurePizza
from dialogFlowSession import DialogFlowSession
from utils import extractDictFromBytesRequest, getJsonCredentialsData
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
client = Client(account_sid, auth_token)
app = Flask(__name__)


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():
    print("a")
    data = extractDictFromBytesRequest()
    receivedMessage = data.get("Body")[0]
    userNumber = data.get("From")[0]
    dialogFlowInstance = DialogFlowSession()
    dialogFlowInstance.sendTwilioMessage(receivedMessage)
    return str(dialogFlowInstance.twiml), 200


@app.route("/dialogFlow", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    print("b")
    requestContent = request.get_json()
    parameters = requestContent['queryResult']['parameters']
    messageContent = requestContent['queryResult']['queryText']
    fullPizza = structurePizza(parameters)
    botResponse = requestContent['queryResult']['fulfillmentText']
    intent = requestContent['queryResult']['intent']
    sessionId = requestContent['session'].split('/')[-1]
    return 'OK', 200


@app.route("/twilioPreEvent", methods=['POST'])
def preEvent():
    """This is a twilio pre-webhook target. It intercepts events, and fires before twilio does anything."""
    print("c")
    data = extractDictFromBytesRequest()
    received_msg = data.get("Body")[0]
    author = data.get("Author")[0].split(":")
    messageService = author[0]
    sender = author[1]
    print('Pre event webhook!')
    return 'OK', 200


# Route to handle incoming Twilio webhook requests for WhatsApp
@app.route('/twilioPostEvent', methods=['POST'])
def handle_whatsapp():
    """This is a twilio post-webhook target. It reacts to changes, and fires after twilio has processed an event.
    It prints on the console the message content and sender."""
    print("d")
    print('Received WhatsApp message!')
    data = extractDictFromBytesRequest()
    sender = data['Author'][0].split(':')[1]
    content = data['Body'][0]
    print(f'Received message from {sender}: {content}')
    return 'OK', 200


# Hello World endpoint
@app.route('/')
def hello():
    return 'Hello, World!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
