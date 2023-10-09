# from gevent import monkey
# monkey.patch_all()

import logging
import os

from flask import request, jsonify, Response, abort
from api_routes.conversation_routes import conversation_blueprint
from api_routes.test_routes import test_blueprint
from api_routes.user_routes import user_blueprint
from orderProcessing.order_builder import buildFullOrder
from orderProcessing.pizza_processor import parsePizzaOrder, convertMultiplePizzaOrderToText
from orderProcessing.drink_processor import structureDrink
from api_config.api_config import app, socketio, dialogFlowInstance
from utils import instagram_utils
from utils.core_utils import updateFirebaseWithUserMessage, processDialogFlowMessage
from utils.helper_utils import extractDictFromBytesRequest, sendTwilioResponse, sendWebhookCallback
import time

from utils.message_utils import convert_dialogflow_message

app.register_blueprint(conversation_blueprint, url_prefix='/conversations')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(test_blueprint, url_prefix='/test')


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():
    start = time.time()
    data: dict = extractDictFromBytesRequest()
    print(data)
    userMessageJSON, chatData = updateFirebaseWithUserMessage(data)
    socketio.start_background_task(target=emitMessage, message=userMessageJSON)
    if 'isHumanActive' in chatData:
        return jsonify({"status": "success", "response": "Message sent"}), 200
    dialogflowMessageJSON = processDialogFlowMessage(userMessageJSON)
    emitMessage(dialogflowMessageJSON)
    response_body = dialogflowMessageJSON["body"]
    print(f"Tempo de execução do envio do socket: {time.time() - start}")
    return sendTwilioResponse(body=response_body, media=None)


@app.route("/testConversation", methods=['POST'])
def conversation_testing():
    body: dict = request.get_json()
    if body is None:
        return "Message cannot be empty", 400
    dialogflowResponse = dialogFlowInstance.getDialogFlowResponse(body)
    dummy_phone_number = "+84932498423"
    dialogflowResponseJSON = convert_dialogflow_message(dialogflowResponse.query_result.fulfillment_text,
                                                        dummy_phone_number)
    botResponse = dialogflowResponseJSON["body"]
    return jsonify(botResponse)


def emitMessage(message):
    socketio.emit('message', message)


@app.route("/webhookForIntent", methods=['POST'])
def send():
    """This is a dialogflow callback endpoint. Everytime a message is sent to the bot, a POST request is sent to this
    endpoint.
    This is under DialogflowEssentials -> Fulfillment"""
    logging.info("FULFILLMENT ENDPOINT")
    requestContent = request.get_json()
    outputContexts = requestContent['queryResult']['outputContexts']
    dialogFlowInstance.params["baseContextName"] = outputContexts[0]['name'].rsplit('/contexts/', 1)[0]
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
        startContext = __structureNewDialogflowContext(contextName="Start", lifespan=1)
        return sendWebhookCallback(botMessage=welcomeString, nextContext=startContext)
    return sendWebhookCallback(botMessage="a")


def __structureNewDialogflowContext(contextName: str, lifespan: int = 5):
    baseContextName = dialogFlowInstance.params["baseContextName"]
    newContext = {
        "name": f"{baseContextName}/contexts/{contextName}",
        "lifespanCount": lifespan,
        "parameters": {}
    }
    return [newContext]


def __handleOrderPizzaIntent(queryText: str, requestContent: dict) -> Response:
    parameters = requestContent['queryResult']['parameters']
    fullPizza = parsePizzaOrder(userMessage=queryText, parameters=parameters)
    fullPizzaText = convertMultiplePizzaOrderToText(fullPizza)
    dialogFlowInstance.params["pizzas"].append(fullPizza)
    followUpContext = __structureNewDialogflowContext("OrderPizza-followup")
    return sendWebhookCallback(botMessage=f"Maravilha! {fullPizzaText.capitalize()} então. "
                                          f"Você vai querer alguma bebida?", nextContext=followUpContext)


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
        headers = list(request.headers)
        is_echo = data['entry'][0]['messaging'][0]['message'].get('is_echo')
        if not is_echo:
            properMessage: dict = instagram_utils.convertIncomingInstagramMessageToProperFormat(data)
            instagram_utils.processInstagramIncomingMessage(properMessage)
        return jsonify({'status': 'success', 'response': 'Message sent'}), 200


def __main():
    port = int(os.environ.get("PORT", 3000))
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    print("API loaded!")
    return


if __name__ == '__main__':
    __main()
