import os

from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client

from analyzePizzaIntent import structurePizza
from dialogFlowSession import DialogFlowSession
from utils import extractDictFromBytesRequest, sendWebhookCallback

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
client = Client(account_sid, auth_token)
app = Flask(__name__)
dialogFlowInstance = DialogFlowSession()


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():
    print("a")
    data = extractDictFromBytesRequest()
    receivedMessage = data.get("Body")[0]
    userNumber = data.get("From")[0]
    dialogflowResponse = dialogFlowInstance.getDialogFlowResponse(receivedMessage)
    dialogFlowInstance.sendTwilioMessage(dialogflowResponse)
    return str(dialogFlowInstance.twiml), 200


@app.route("/webhookForIntent", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    requestContent = request.get_json()
    parameters = requestContent['queryResult']['parameters']
    flavor = parameters["flavor"][0] if parameters.get("flavor") else None
    number = parameters["number"][0] if parameters.get("number") else None
    if not number:
        return sendWebhookCallback(desiredMessage=f"Só pra confirmar: seria uma pizza inteira de {flavor}, certo?",
                                   newIntent="Order.pizza - yes")
    fullPizza = structurePizza(parameters)
    botResponse = requestContent['queryResult']['fulfillmentText']
    intent = requestContent['queryResult']['intent']
    sessionId = requestContent['session'].split('/')[-1]
    receivedMessage = requestContent['queryResult']['queryText']
    return sendWebhookCallback(desiredMessage=f"Maravilha! Uma {fullPizza} então.")


@app.route("/staticReply", methods=['POST'])
def staticReply():
    return sendWebhookCallback("This is a message from the server!")


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


@app.route("/watsonAssistant", methods=['POST'])
def handle_watson():
    print("d")
    return 'OK', 200


# Hello World endpoint
@app.route('/')
def hello():
    return 'Hello, World!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
