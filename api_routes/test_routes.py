# routes/conversation_routes.py
import json

from flask import Blueprint, jsonify, request

from api_config.api_config import fcm, socketio
from data.message_converter import get_dialogflow_message_example, MessageConverterObject, get_user_message_example
from socketEmissions.socket_emissor import pulseEmit
from utils.helper_utils import __getUserByWhatsappNumber

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route("/chatTest", methods=['GET'])
def chatTest():
    dialogflow_message = get_dialogflow_message_example()
    user_message = get_user_message_example()
    userMessageJSON = MessageConverterObject.convertUserMessage(user_message)

    dialogFlowJSON = MessageConverterObject.convert_dialogflow_message(dialogflow_message, userMessageJSON['phoneNumber'])
    for _ in range(4):
        pulseEmit(socketio, userMessageJSON)
        pulseEmit(socketio, dialogFlowJSON)
    return [], 200

