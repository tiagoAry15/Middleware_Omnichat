from flask import Blueprint, jsonify, request

from api_config.api_config import fo

order_blueprint = Blueprint('orders', __name__)


@order_blueprint.route("/create_order", methods=['POST'])
def create_order():
    data = request.get_json()
    response = fo.createOrder(data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@order_blueprint.route("/get_order/<string:order_unique_id>", methods=['GET'])
def get_order(order_unique_id):
    data = fo.getOrder(order_unique_id)
    return jsonify(data), 200


@order_blueprint.route("/get_all_orders", methods=['GET'])
def get_all_orders():
    data = fo.getAllOrders()
    trimmedData = list(data.values()) if data else None
    return jsonify(trimmedData), 200


@order_blueprint.route("/update_order/<string:order_unique_id>", methods=['PUT'])
def update_order(order_unique_id):
    data = request.get_json()
    response = fo.updateOrder(order_unique_id, data)
    finalResponse = data if response else False
    return jsonify(finalResponse), 200


@order_blueprint.route("/delete_order/<string:order_unique_id>", methods=['DELETE'])
def delete_order(order_unique_id):
    response = fo.deleteOrder(order_unique_id)
    return jsonify(response), 200
