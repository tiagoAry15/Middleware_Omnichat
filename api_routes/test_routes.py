# routes/conversation_routes.py
import json

from flask import Blueprint, jsonify, request

from api_config.api_setup import socketio
from api_config.object_factory import fcm
from data.message_converter import get_dialogflow_message_example, get_user_message_example
from socketEmissions.socket_emissor import pulseEmit
from utils.helper_utils import __getUserByWhatsappNumber, sendWebhookCallback
from utils.message_utils import convert_dialogflow_message, convertUserMessage

test_blueprint = Blueprint('test', __name__)


@test_blueprint.route("/chatTest", methods=['GET'])
def chatTest():
    dialogflow_message = get_dialogflow_message_example()
    user_message = get_user_message_example()
    userMessageJSON = convertUserMessage(user_message)
    dialogFlowJSON = convert_dialogflow_message(dialogflow_message, userMessageJSON['phoneNumber'])
    for _ in range(4):
        pulseEmit(socketio, userMessageJSON)
        pulseEmit(socketio, dialogFlowJSON)
    return [], 200


@test_blueprint.route("/staticReply", methods=['POST'])
def staticReply():
    return sendWebhookCallback("This is a message from the server!")
