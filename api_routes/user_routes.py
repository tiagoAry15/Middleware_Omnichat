import json

from flask import Blueprint, jsonify, request

from api_config.api_config import fcm
from utils.helper_utils import __getUserByWhatsappNumber

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/get_all_users", methods=['GET'])
def get_all_users():
    data = fcm.getAllUsers()
    trimmedData = list(data.values()) if data else None
    return jsonify(trimmedData), 200


@user_blueprint.route("/get_user_by_whatsapp_number", methods=['GET'])
def get_user_by_whatsapp_number():
    data = json.loads(request.data.decode("utf-8"))
    whatsappNumber = data.get("whatsappNumber", None)
    userData = fcm.getUserByWhatsappNumber(whatsappNumber)
    return jsonify(userData), 200


@user_blueprint.route("/create_user", methods=['POST'])
def create_user():
    print("Creating new user!")
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.createUser(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@user_blueprint.route("/update_user", methods=['PUT'])
def update_user():
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.updateUser(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@user_blueprint.route("/delete_user", methods=['DELETE'])
def delete_user():
    data = json.loads(request.data.decode("utf-8"))
    response = fcm.deleteUser(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200
