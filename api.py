import logging
from flask import request, jsonify, Response, abort
from api_routes.conversation_routes import conversation_blueprint
from api_routes.test_routes import test_blueprint
from api_routes.user_routes import user_blueprint
from orderProcessing.order_handler import structureDrink, buildFullOrder, parsePizzaOrder, \
    convertMultiplePizzaOrderToText
from socketEmissions.socket_emissor import pulseEmit
from api_config.api_config import app, socketio, dialogFlowInstance, fu, mc, twilioClient, twilio_phone_number
from utils import instagram_utils
from utils.core_utils import processUserMessage, processDialogFlowMessage
from utils.helper_utils import extractDictFromBytesRequest, sendTwilioResponse, sendWebhookCallback
import time
from twilio.rest import Client

app.register_blueprint(conversation_blueprint, url_prefix='/conversations')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(test_blueprint, url_prefix='/test')


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():
    start = time.time()
    data: dict = extractDictFromBytesRequest()
    print(data)
    userMessageJSON, chatData = processUserMessage(data)
    socketio.start_background_task(target=emitMessage, message=userMessageJSON)
    if 'isHumanActive' in chatData:
        return jsonify({"status": "success", "response": "Message sent"}), 200
    dialogflowMessageJSON = processDialogFlowMessage(userMessageJSON)
    emitMessage(dialogflowMessageJSON)
    response_body = dialogflowMessageJSON["body"]
    print(f"Tempo de execução do envio do socket: {time.time() - start}")
    return sendTwilioResponse(body=response_body, media=None)





def emitMessage(message):
    socketio.emit('message', message)


@app.route("/webhookForIntent", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    logging.info("FULFILLMENT ENDPOINT")
    dialogFlowInstance.params["secret"] = "Mensagem secreta"
    requestContent = request.get_json()
    contexts = [item['name'].split("/")[-1] for item in requestContent['queryResult']['outputContexts']]
    queryText = requestContent['queryResult']['queryText']
    userMessage = [item["name"] for item in queryText] if isinstance(queryText, list) else queryText
    # socketMessage = mc.dynamicConversion(userMessage)
    # socketInstance.emit('message', socketMessage)
    # pulseEmit(socketio, socketMessage)
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
            instagram_utils.processInstagramIncomingMessage(data)
        return jsonify({'status': 'success', 'response': 'Message sent'}), 200


def __main():
    app.debug = False
    socketio.run(app, host='0.0.0.0', port=3000, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    __main()
