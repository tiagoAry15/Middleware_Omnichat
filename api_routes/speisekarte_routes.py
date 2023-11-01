from flask import Blueprint, request

from api_config.object_factory import fs

speisekarte_blueprint = Blueprint('speisekarte', __name__)


@speisekarte_blueprint.route("/create_menu", methods=['POST'])
def create_menu():
    if request.method != "POST":
        return "This endpoint only accepts POST requests", 405
    body_dict = request.get_json()
    result = fs.createSpeisekarte(speisekarte_data=body_dict)
    if result:
        return "Speisekarte created successfully", 200
    return "Speisekarte already exists", 200


@speisekarte_blueprint.route("/get_menu_by_author/<author>", methods=['GET'])
def get_menu_by_author(author):
    if request.method != "GET":
        return "This endpoint only accepts GET requests", 405
    speisekarte_data = fs.read_speisekarte(author=author)
    if not speisekarte_data:
        return "Speisekarte not found", 404
    return speisekarte_data, 200


@speisekarte_blueprint.route("/update_menu_by_author/<author>", methods=['PUT'])
def update_menu_by_author(author):
    if request.method != "PUT":
        return "This endpoint only accepts PUT requests", 405
    body_dict = request.get_json()
    result = fs.update_speisekarte(author=author, newData=body_dict)
    if not result:
        return "Speisekarte not found", 404
    return "Speisekarte updated successfully", 200


@speisekarte_blueprint.route("/delete_menu_by_author/<author>", methods=['DELETE'])
def delete_menu_by_author(author):
    if request.method != "DELETE":
        return "This endpoint only accepts DELETE requests", 405
    result = fs.delete_speisekarte(author=author)
    if not result:
        return "Speisekarte not found", 404
    return "Speisekarte deleted successfully", 200
