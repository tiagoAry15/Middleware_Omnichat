import datetime
import logging
import os
import requests
from flask import request, jsonify, Response, abort
from data.message_converter import MessageConverter, get_dialogflow_message_example, get_user_message_example
from firebaseFolder.firebase_conversation import getDummyConversationDicts
from orderProcessing.order_handler import structureDrink, buildFullOrder, parsePizzaOrder, \
    convertMultiplePizzaOrderToText
from gpt.pizza_gpt import getResponseDefaultGPT
from socketEmissions.socket_emissor import pulseEmit
import json
from api.api_config import app, socketInstance, dialogFlowInstance, fu, fcm, mc
from utils.core_utils import processTwilioSandboxIncomingMessage
from utils.helper_utils import extractDictFromBytesRequest, sendTwilioResponse, sendWebhookCallback, \
    __getUserByWhatsappNumber

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():  # sourcery skip: use-named-expression
    data = extractDictFromBytesRequest()
    mainResponseDict = processTwilioSandboxIncomingMessage(data)
    rawResponse = mainResponseDict["body"]

    image_url = "https://shorturl.at/lEFT0"
    pulseEmit(socketInstance, mainResponseDict)
    return sendTwilioResponse(body=rawResponse, media=None)


@app.route("/chatTest", methods=['GET'])
def chatTest():
    dialogflow_message = get_dialogflow_message_example()
    user_message = get_user_message_example()
    userMessageJSON = MessageConverter.convertUserMessage(user_message)

    dialogFlowJSON = MessageConverter.convert_dialogflow_message(dialogflow_message, userMessageJSON['phoneNumber'])
    for _ in range(4):
        pulseEmit(socketInstance, userMessageJSON)
        pulseEmit(socketInstance, dialogFlowJSON)
    return [], 200


@app.route("/webhookForIntent", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    logging.info("FULLFILLMENT ENDPOINT")
    dialogFlowInstance.params["secret"] = "Mensagem secreta"
    requestContent = request.get_json()
    contexts = [item['name'].split("/")[-1] for item in requestContent['queryResult']['outputContexts']]
    queryText = requestContent['queryResult']['queryText']
    userMessage = [item["name"] for item in queryText] if isinstance(queryText, list) else queryText
    socketMessage = mc.dynamicConversion(userMessage)
    # socketInstance.emit('message', socketMessage)
    pulseEmit(socketInstance, socketMessage)
    currentIntent = requestContent['queryResult']['intent']['displayName']
    logging.info(f"current Intent: {currentIntent}")
    params = requestContent['queryResult']['parameters']
    if currentIntent == "Order.drink":
        return __handleOrderDrinkIntent(params, userMessage)
    elif currentIntent == "Order.pizza - drink no":
        params = dialogFlowInstance.params
        fullOrder = buildFullOrder(params)
        totalPriceDict = dialogFlowInstance.analyzeTotalPrice(fullOrder)
        finalMessage = totalPriceDict["finalMessage"]
        return sendWebhookCallback(finalMessage)
    elif currentIntent == "Order.pizza - drink yes":
        drinkString = dialogFlowInstance.getDrinksString()
        return sendWebhookCallback(drinkString)
    elif currentIntent == "Order.pizza":
        return __handleOrderPizzaIntent(queryText, requestContent)
    elif currentIntent == "Welcome":
        pizzaMenu = dialogFlowInstance.getPizzasString()
        welcomeString = f"Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n {pizzaMenu}." \
                        f" \nQual pizza você vai querer?"
        return sendWebhookCallback(welcomeString)
    return sendWebhookCallback(botMessage="a")


def __handleOrderPizzaIntent(queryText: str, requestContent: dict) -> Response:
    parameters = requestContent['queryResult']['parameters']
    fullPizza = parsePizzaOrder(userMessage=queryText, parameters=parameters)
    fullPizzaText = convertMultiplePizzaOrderToText(fullPizza)
    dialogFlowInstance.params["pizzas"].append(fullPizza)
    return sendWebhookCallback(botMessage=f"Maravilha! {fullPizzaText.capitalize()} então. "
                                          f"Você vai querer alguma bebida?")


def __handleOrderDrinkIntent(params: dict, userMessage: str) -> Response:
    drink = structureDrink(params, userMessage)
    dialogFlowInstance.params["drinks"].append(drink)
    parameters = dialogFlowInstance.params
    fullOrder = buildFullOrder(parameters)
    totalPriceDict = dialogFlowInstance.analyzeTotalPrice(fullOrder)
    finalMessage = totalPriceDict["finalMessage"]
    return sendWebhookCallback(finalMessage)


@app.route("/get_all_users", methods=['GET'])
def get_all_users():
    aux = fu.getAllUsers()
    return jsonify(aux), 200


@app.route("/get_user/<whatsapp_number>", methods=['GET'])
def get_user_by_whatsapp(whatsapp_number: str):
    user = __getUserByWhatsappNumber(whatsapp_number)
    return ((jsonify(user), 200) if user
            else (jsonify({"Error": f"Could not find an user with whatsapp {whatsapp_number}"}), 404))


@app.route("/delete_user/<whatsapp_number>", methods=['DELETE'])
def delete_user_by_whatsapp(whatsapp_number: str):
    user = __getUserByWhatsappNumber(whatsapp_number)
    if not user:
        return jsonify({"Error": f"Could not find an user with whatsapp {whatsapp_number}"}), 404
    fu.deleteUser(user)
    return jsonify({"Success": f"User with whatsapp {whatsapp_number} deleted"}), 200


@app.route("/get_user_conversations/<whatsapp_number>", methods=['GET'])
def get_user_conversations_by_whatsapp(whatsapp_number: str):
    response = fcm.retrieveAllMessagesByWhatsappNumber(whatsapp_number)
    # if response is None:
    #     response = fcm.createFirstDummyConversationByWhatsappNumber(whatsapp_number)
    return ((jsonify(response), 200)
            if response
            else (
        jsonify({"Error": f"Could not find conversations for the user with whatsapp {whatsapp_number}"}), 404))


@app.route("/add_message", methods=['POST'])
def add_message():
    data = json.loads(request.data)
    whatsapp_number = data['phoneNumber']

    response = fcm.appendMessageToWhatsappNumber(
        messageData=data, whatsappNumber=whatsapp_number
    )
    return jsonify(response), 200


@app.route("/push_new_message_by_whatsapp_number/", methods=['POST'])
def push_new_message_by_whatsapp_number():
    data = dict(request.form)
    whatsapp_number = data.get("whatsapp")
    user = __getUserByWhatsappNumber(whatsapp_number)
    if not user:
        return jsonify({"Error": f"Could not find an user with whatsapp {whatsapp_number}"}), 404
    conversations = fcm.retrieveAllMessagesByWhatsappNumber(whatsapp_number)
    # if not conversations:
    #     return jsonify({"Error": f"Could not find conversations for the user with whatsapp {whatsapp_number}"}), 404
    message = {"content": data.get("message")}
    fcm.appendMessageToWhatsappNumber(messageData=message, whatsappNumber=whatsapp_number)
    return jsonify({"Success": f"New message pushed for user with whatsapp {whatsapp_number}"}), 200


@app.route("/create_conversation", methods=['POST'])
def create_conversation():
    print("Creating new conversation!")
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.createConversation(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@app.route("/create_dummy_conversation", methods=['POST'])
def create_dummy_conversation():
    data = json.loads(request.data.decode("utf-8"))
    dummyMessagePot, dummyPot = getDummyConversationDicts().values()
    for message in dummyPot:
        fcm.createConversation(message)
    return jsonify({"Success": "Dummy conversation created"}), 200


@app.route("/update_conversation", methods=['PUT'])
def update_conversation():
    messageData = json.loads(request.data.decode("utf-8"))
    response = fcm.updateConversationAddingUnreadMessages(messageData)
    return jsonify(response), 200


@app.route("/get_all_conversations", methods=['GET'])
def get_all_conversations():
    data = fcm.getAllConversations()
    trimmedData = list(data.values()) if data else None
    return jsonify(trimmedData), 200


@app.route("/staticReply", methods=['POST'])
def staticReply():
    return sendWebhookCallback("This is a message from the server!")


@app.route("/twilioPreEvent", methods=['POST'])
def preEvent():
    """This is a twilio pre-webhook target. It intercepts events, and fires before twilio does anything."""
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
    data = extractDictFromBytesRequest()
    sender = data['Author'][0].split(':')[1]
    content = data['Body'][0]
    return 'OK', 200


@app.route('/twilioSandboxGPT', methods=['POST'])
def handle_response():
    data = extractDictFromBytesRequest()
    receivedMessage = data.get("Body")[0]
    mainResponse = getResponseDefaultGPT(receivedMessage)
    image_url = "https://shorturl.at/lEFT0"
    return sendTwilioResponse(body=mainResponse)


@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe':
            return request.args.get('hub.challenge')
        else:
            abort(403)
    if request.method == 'POST':
        # Handle POST requests here (i.e. updates from Instagram)
        data = request.get_json()
        is_echo = data['entry'][0]['messaging'][0]['message'].get('is_echo')
        if not is_echo:
            _processInstagramIncomingMessage(data)
        return jsonify({'status': 'success', 'response': 'Message sent'}), 200


def _processInstagramIncomingMessage(data):
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    message_text = data['entry'][0]['messaging'][0]['message']['text']
    structuredMessage = {'Body': [message_text], 'From': [f'whatsapp:+5585{sender_id}'], 'ProfileName': [sender_id]}
    mainResponse = processTwilioSandboxIncomingMessage(structuredMessage)
    txtResponse = mainResponse["body"]
    __sendInstagramMessage(sender_id, txtResponse)
    currentFormattedTime = datetime.datetime.now().strftime("%H:%M")
    emitDict = {'body': message_text, 'from': 'instagram', 'phoneNumber': sender_id, 'sender': 'Mateus',
                'time': currentFormattedTime}
    # socketInstance.emit('message', emitDict)
    pulseEmit(socketInstance, emitDict)


def __sendInstagramMessage(recipient_id, message_text):
    access_token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
    headers = {'Content-Type': 'application/json'}
    data = {'recipient': {'id': recipient_id}, 'message': {'text': message_text}}
    params = {'access_token': access_token}
    response = requests.post('https://graph.facebook.com/v13.0/me/messages', headers=headers, params=params, json=data)
    if response.status_code != 200:
        print(f"Unable to send message: {response.text}")


def __main():
    socketInstance.run(app=app, port=3000, host="0.0.0.0", debug=True)


if __name__ == '__main__':
    __main()
