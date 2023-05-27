import os

from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client

from orderProcessing.orderHandler import structureDrink, structureFullOrder, parsePizzaOrder, \
    convertPizzaOrderToText
from dialogFlowSession import DialogFlowSession
from gpt.PizzaGPT import getResponseDefaultGPT
from intentManipulation.intentManager import IntentManager
from utils import extractDictFromBytesRequest, sendWebhookCallback, changeDialogflowIntent, _sendTwilioResponse

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
client = Client(account_sid, auth_token)
app = Flask(__name__)
dialogFlowInstance = DialogFlowSession()


def __handleWelcomeMultipleOptions(parameters: dict):
    chosenNumber = int(parameters["number"][0])
    if chosenNumber == 1:
        dialogFlowInstance.sendTwilioRawMessage("Qual pizza você vai querer hoje?")
        return sendWebhookCallback("Qual pizza você vai querer hoje?")
    if chosenNumber == 2:
        dialogFlowInstance.sendTwilioRawMessage("Aqui está o cardápio!", image_url="https://shorturl.at/lEFT0")
        return changeDialogflowIntent("Order.pizza")
    elif chosenNumber == 3:
        dialogFlowInstance.sendTwilioRawMessage("Nós funcionamos das 17h até as 22h")
        return changeDialogflowIntent("Order.pizza")


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():  # sourcery skip: use-named-expression
    data = extractDictFromBytesRequest()
    receivedMessage = data.get("Body")[0]
    userNumber = data.get("From")[0]

    im = IntentManager()
    needsToSignUp = im.needsToSignUp(userNumber)
    if needsToSignUp:
        im.extractedParameters["phoneNumber"] = userNumber
        botAnswer = im.twilioSingleStep(receivedMessage)
        return _sendTwilioResponse(body=botAnswer)

    dialogflowResponse = dialogFlowInstance.getDialogFlowResponse(receivedMessage)
    secret = dialogFlowInstance.params.get("secret")
    detectedIntent = dialogflowResponse.query_result.intent.display_name
    # IntentManager.process_intent(detectedIntent)
    parameters = dict(dialogflowResponse.query_result.parameters)
    mainResponse = dialogFlowInstance.extractTextFromDialogflowResponse(dialogflowResponse)
    image_url = "https://shorturl.at/lEFT0"
    return _sendTwilioResponse(body=mainResponse, media=None)


@app.route("/webhookForIntent", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    print('FULFILLMENT ATIVADO')
    dialogFlowInstance.params["secret"] = "Mensagem secreta"
    requestContent = request.get_json()
    contexts = [item['name'].split("/")[-1] for item in requestContent['queryResult']['outputContexts']]
    queryText = requestContent['queryResult']['queryText']
    userMessage = [item["name"] for item in queryText] if isinstance(queryText, list) else queryText
    currentIntent = requestContent['queryResult']['intent']['displayName']
    print(f"current Intent: {currentIntent}")
    if currentIntent == "Order.drink":
        params = requestContent['queryResult']['parameters']
        drink = structureDrink(params, userMessage)
        dialogFlowInstance.params["drinks"].append(drink)
        fullOrder = structureFullOrder(dialogFlowInstance.params)
        totalPriceDict = dialogFlowInstance.analyzeTotalPrice(fullOrder)
        finalMessage = totalPriceDict["finalMessage"]
        return sendWebhookCallback(finalMessage)
    elif currentIntent == "Order.pizza - drink no":
        params = dialogFlowInstance.params
        fullOrder = structureFullOrder(dialogFlowInstance.params)
        totalPriceDict = dialogFlowInstance.analyzeTotalPrice(fullOrder)
        finalMessage = totalPriceDict["finalMessage"]
        return sendWebhookCallback(finalMessage)
    elif currentIntent == "Order.pizza - drink yes":
        drinkString = dialogFlowInstance.getDrinksString()
        return sendWebhookCallback(drinkString)
    elif currentIntent == "Order.pizza":
        parameters = requestContent['queryResult']['parameters']
        flavor = parameters["flavor"][0] if parameters.get("flavor") else None
        number = parameters["number"][0] if parameters.get("number") else None
        if not number:
            parameters["number"] = [1.0]
        # fullPizza = "inteira calabresa"
        fullPizza = parsePizzaOrder(userMessage=queryText, parameters=parameters)
        fullPizzaText = convertPizzaOrderToText(fullPizza)
        dialogFlowInstance.params["pizzas"].append(fullPizza)
        return sendWebhookCallback(botMessage=f"Maravilha! {fullPizzaText.capitalize()} então. "
                                              f"Você vai querer alguma bebida?")
    elif currentIntent == "Welcome":
        pizzaMenu = dialogFlowInstance.getPizzasString()
        welcomeString = f"Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n {pizzaMenu}." \
                        f" \nQual pizza você vai querer?"
        return sendWebhookCallback(welcomeString)
    return sendWebhookCallback(botMessage="a")


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


@app.route('/twilioSandboxGPT', methods=['POST'])
def handle_response():
    data = extractDictFromBytesRequest()
    receivedMessage = data.get("Body")[0]
    mainResponse = getResponseDefaultGPT(receivedMessage)
    image_url = "https://shorturl.at/lEFT0"
    return _sendTwilioResponse(body=mainResponse)


# Hello World endpoint
@app.route('/')
def hello():
    return 'Hello, World!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
