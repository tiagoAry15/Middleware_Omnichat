# routes/conversation_routes.py
import json

from flask import Blueprint, jsonify, request
from api_config.api_setup import twilioClient, twilio_phone_number
from api_config.object_factory import fcm
from utils.helper_utils import __getUserByWhatsappNumber

conversation_blueprint = Blueprint('conversation', __name__)


@conversation_blueprint.route("/get_all_conversations", methods=['GET'])
def get_all_conversations():
    data = fcm.getAllConversations()
    trimmedData = list(data.values()) if data else None
    return jsonify(trimmedData), 200


@conversation_blueprint.route("/get_conversation_by_whatsapp_number/<whatsappNumber>", methods=['GET'])
def get_conversation_by_whatsapp_number(whatsappNumber):
    conversationData = fcm.getConversationByWhatsappNumber(whatsappNumber)
    return jsonify(conversationData), 200


@conversation_blueprint.route("/create_conversation", methods=['POST'])
def create_conversation():
    print("Creating new conversation!")
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.createConversation(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@conversation_blueprint.route("/update_conversation", methods=['PUT'])
def update_conversation():
    try:
        print('updating')
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        response = fcm.updateConversation(data)

        if response:
            return jsonify({"success": True, "data": data}), 200
        else:
            return jsonify({"success": False, "error": "Failed to update, conversation does not exist"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": e}), 500


@conversation_blueprint.route("/update_conversation_adding_unread_messages", methods=['PUT'])
def update_conversation_adding_unread_messages():
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.updateConversationAddingUnreadMessages(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@conversation_blueprint.route("/delete_conversation", methods=['DELETE'])
def delete_conversation():
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.deleteConversation(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@conversation_blueprint.route("/push_new_message_by_whatsapp_number/", methods=['POST'])
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
    fcm.appendMessageToConversation(messageData=message, whatsappNumber=whatsapp_number)
    return jsonify({"Success": f"New message pushed for user with whatsapp {whatsapp_number}"}), 200
