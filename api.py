# from gevent import monkey
# monkey.patch_all()

import logging
import os
from flask import request, jsonify, abort
from werkzeug.exceptions import BadRequest

from api_routes.conversation_routes import conversation_blueprint
from api_routes.order_routes import order_blueprint
from api_routes.speisekarte_routes import speisekarte_blueprint
from api_routes.test_routes import test_blueprint
from api_routes.user_routes import user_blueprint
from dialogflowFolder.dialogflow_session import DialogflowSession
from intentProcessing.core_intent_processing import fulfillment_processing
from api_config.api_config import app, socketio
from api_config.object_factory import dialogflowConnectionManager
from utils import instagram_utils
from utils.core_utils import extractMetaDataFromTwilioCall, appendMultipleMessagesToFirebase
from utils.cors_blocker import get_anti_cors_headers
from utils.helper_utils import extractDictFromBytesRequest
from utils.instagram_utils import extractMetadataFromInstagramDict

app.register_blueprint(conversation_blueprint, url_prefix='/conversations')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(test_blueprint, url_prefix='/test')
app.register_blueprint(speisekarte_blueprint, url_prefix='/speisekarte')
app.register_blueprint(order_blueprint, url_prefix='/orders')


@app.route("/twilioSandbox", methods=['POST'])
def sandbox():
    try:
        data: dict = extractDictFromBytesRequest()
        print("TWILIO SANDBOX ENDPOINT!")
        metaData = extractMetaDataFromTwilioCall(data)
        ip_address = request.remote_addr
        userMessage = str(data["Body"][0])
        botResponse = _get_bot_response_from_user_session(user_message=userMessage, ip_address=ip_address)
        # appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
        socketio.start_background_task(target=emitMessage, message=botResponse)
        return botResponse
    except Exception as e:
        print(e)
        logging.error(e)
        return f'Erro ao receber a mensagem, por favor tente novamente em instantes! {e}'


@app.route("/webhookForIntent", methods=['POST'])
def send():
    try:
        requestContent = request.get_json()
        return fulfillment_processing(requestContent)
    except Exception as e:
        print(e)
        logging.error(e)
        return 'Erro no processamento de resposta do Bot, tente novamente em instantes!'


def emitMessage(message):
    socketio.emit('message', message)


def emitOrder(order):
    socketio.emit('order', order)


@app.route("/testDialogflow", methods=["POST"])
def dialogflow_testing():
    headers = get_anti_cors_headers()
    try:
        body: str = request.get_json()
    except BadRequest:
        return "Message cannot be empty. Try sending a JSON object with any string message.", 400
    ip_address = request.remote_addr
    bot_answer = _get_bot_response_from_user_session(user_message=body, ip_address=ip_address)
    print(bot_answer)
    if bot_answer == "":
        return (f"Could not find any response from Dialogflow for the message '{body}'."
                f" Check if your message is valid."), 400
    return bot_answer, 200, headers


def _get_bot_response_from_user_session(user_message: str, ip_address: str):
    user_instance: DialogflowSession = dialogflowConnectionManager.get_instance_session(ip_address)
    user_instance.initialize_session(ip_address)
    response = user_instance.getDialogFlowResponse(message=user_message)
    bot_answer = response.query_result.fulfillment_text
    return bot_answer


@app.route("/eraseSession", methods=["PUT"])
def erase_session():
    if request.method != "PUT":
        return "This endpoint only accepts PUT requests", 405
    ip_address = request.remote_addr
    dialogflowConnectionManager.erase_session(ip_address)
    return "Session erased", 200


@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    try:
        if request.method == 'GET':
            if request.args.get('hub.mode') == 'subscribe':
                return request.args.get('hub.challenge')
            else:
                abort(403)
        if request.method == 'POST':
            # Handle POST requests here (i.e. updates from Instagram)
            data = request.get_json()
            headers = list(request.headers)
            ip_address = request.remote_addr
            is_echo = data['entry'][0]['messaging'][0]['message'].get('is_echo')
            if not is_echo:
                properMessage: dict = instagram_utils.convertIncomingInstagramMessageToProperFormat(data)
                metaData = extractMetadataFromInstagramDict(properMessage)
                userMessage = str(properMessage["Body"][0])
                botResponse = _get_bot_response_from_user_session(user_message=userMessage, ip_address=ip_address)
                appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
            return jsonify({'status': 'success', 'response': 'Message sent'}), 200
    except Exception as e:
        print(e)
        logging.error(e)
        return jsonify({'status': 'failed', 'response': 'Message not sent'}), 400


@app.route("/pizzaMenuUpdate", methods=['POST'])
def pizza_menu_update():
    if request.method != "POST":
        return "This endpoint only accepts POST requests", 405
    body_dict = request.get_json()


def __main():
    port = int(os.environ.get("PORT", 3000))
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    print("API loaded!")
    return


if __name__ == '__main__':
    __main()
