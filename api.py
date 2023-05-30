import os

from dotenv import load_dotenv
from flask import Flask, request
from twilio.rest import Client
from flask_socketio import SocketIO
from analyzePizzaIntent import structurePizza, structureDrink, structureFullOrder
from dialogFlowSession import DialogFlowSession
from gpt.PizzaGPT import getResponseDefaultGPT
from intentManipulation.intentManager import IntentManager
from messageConverter import MessageConverter
from utils import extractDictFromBytesRequest, sendWebhookCallback, changeDialogflowIntent, _sendTwilioResponse
from flask_cors import CORS

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
client = Client(account_sid, auth_token)
app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')

dialogFlowInstance = DialogFlowSession()


@socketio.on('sendMessage')
def handle_message(msg):
    print('mensagem recebida com sucesso')
    socketio.emit('receiveMessage', 'oi flask')


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
    userMessageJSON = MessageConverter.convert_user_message(data)
    socketio.emit('user_message', userMessageJSON)

    im = IntentManager()
    needsToSignUp = im.needsToSignUp(userNumber)
    if needsToSignUp:
        im.extractedParameters["phoneNumber"] = userNumber
        botAnswer = im.twilioSingleStep(receivedMessage)
        return _sendTwilioResponse(body=botAnswer)

    dialogflowResponse = dialogFlowInstance.getDialogFlowResponse(receivedMessage)
    dialogflowResponseJSON = MessageConverter.convert_dialogflow_message(dialogflowResponse)
    socketio.emit('dialogflow_message', userMessageJSON)
    secret = dialogFlowInstance.params.get("secret")
    detectedIntent = dialogflowResponse.query_result.intent.display_name
    # IntentManager.process_intent(detectedIntent)
    parameters = dict(dialogflowResponse.query_result.parameters)
    mainResponse = dialogFlowInstance.extractTextFromDialogflowResponse(dialogflowResponse)
    image_url = "https://shorturl.at/lEFT0"
    socketio.emit('Bot_response', dialogflowResponseJSON)

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
    if currentIntent == "Order.pizza - drink yes":
        drinkString = dialogFlowInstance.getDrinksString()
        return sendWebhookCallback(drinkString)
    elif currentIntent == "Welcome":
        pizzaMenu = dialogFlowInstance.getPizzasString()
        welcomeString = f"Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n {pizzaMenu}." \
                        f" \nQual pizza você vai querer?"
        return sendWebhookCallback(welcomeString)
    elif currentIntent == "Order.drink":
        params = requestContent['queryResult']['parameters']
        drink = structureDrink(params)
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
    elif currentIntent == "Order.pizza":
        parameters = requestContent['queryResult']['parameters']
        flavor = parameters["flavor"][0] if parameters.get("flavor") else None
        number = parameters["number"][0] if parameters.get("number") else None
        if not number:
            parameters["number"] = [1.0]
        fullPizza = structurePizza(parameters)
        dialogFlowInstance.params["pizzas"].append(fullPizza)
        return sendWebhookCallback(botMessage=f"Maravilha! Uma {fullPizza} então. Você vai querer alguma bebida?")
    return sendWebhookCallback(botMessage="a")


@app.route("/ChaTtest", methods=['GET'])
def chatTest():
    dialogflow_message = {
        "response_id": "db1b18cf-4ed9-4339-bcfd-725cf722b4b7-4c6e80df",
        "query_result": {
            "query_text": "Oi",
            "language_code": "pt-br",
            "action": "input.welcome",
            "parameters": {
                "fields": {
                    "key": "time-period",
                    "value": {
                        "string_value": ""
                    }
                },
                "fields": {
                    "key": "location",
                    "value": {
                        "struct_value": {
                            "fields": {
                                "key": "zip-code",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "subadmin-area",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "street-address",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "shortcut",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "island",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "country",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "city",
                                "value": {
                                    "string_value": ""
                                }
                            },
                            "fields": {
                                "key": "business-name",
                                "value": {
                                    "string_value": "Oi"
                                }
                            },
                            "fields": {
                                "key": "admin-area",
                                "value": {
                                    "string_value": ""
                                }
                            }
                        }
                    }
                },
                "fields": {
                    "key": "date-time",
                    "value": {
                        "string_value": ""
                    }
                }
            },
            "all_required_params_present": "True",
            "fulfillment_text": "Por favor, ligue a API",
            "fulfillment_messages": {
                "text": {
                    "text": "Por favor, ligue a API"
                }
            },
            "intent": {
                "name": "projects/pizzadobill-rpin/agent/intents/acd8e087-5400-4cf9-95f3-4c681b16b516",
                "display_name": "Welcome"
            },
            "intent_detection_confidence": 1,
            "diagnostic_info": {
                "fields": {
                    "key": "webhook_latency_ms",
                    "value": {
                        "number_value": 2889
                    }
                }
            }
        },
        "webhook_status": {
            "code": 14,
            "message": "Webhook call failed. Error: UNAVAILABLE, State: URL_UNREACHABLE, Reason: UNREACHABLE_5xx, HTTP status code: 502."
        }
    }
    user_message = {
        "SmsMessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "NumMedia": ["0"],
        "ProfileName": ["Tiago Ary"],
        "SmsSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "WaId": ["558599663533"],
        "SmsStatus": ["received"],
        "Body": ["Oi"],
        "To": ["whatsapp:+14155238886"],
        "NumSegments": ["1"],
        "ReferralNumMedia": ["0"],
        "MessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "AccountSid": ["AC034f7d97b8d5bc62dfa91b519ac43b0f"],
        "From": ["whatsapp:+558599663533"],
        "ApiVersion": ["2010-04-01"]
    }
    userMessageJSON = MessageConverter.convert_user_message(user_message)

    dialogFlowJSON = MessageConverter.convert_dialogflow_message(dialogflow_message, userMessageJSON['telephone'])
    for i in range(0, 4):
        socketio.emit('user_message', userMessageJSON)
        socketio.emit('dialogflow_message', dialogFlowJSON)


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
    socketio.run(app, port=8000)
