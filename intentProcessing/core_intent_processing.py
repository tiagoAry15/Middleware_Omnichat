import logging

from flask import Response

from api_config.object_factory import menuHandler
from global_object.global_object_utils import get_all_users_from_global_object
from intentProcessing.order_factory import format_order_data, build_socket_object
from orderProcessing.drink_processor import structureDrink
from orderProcessing.order_builder import buildFullOrder
from orderProcessing.pizza_processor import parsePizzaOrder, convertMultiplePizzaOrderToText
from api_config.api_setup import send_message
from utils.dialogflow_utils import structureNewDialogflowContext, create_session
from utils.helper_utils import sendWebhookCallback


async def fulfillment_processing(requestContent):
    outputContexts = requestContent['queryResult']['outputContexts']
    menuHandler.params["baseContextName"] = outputContexts[0]['name'].rsplit('/contexts/', 1)[0]
    queryText = requestContent['queryResult']['queryText']
    userMessage = [item["name"] for item in queryText] if isinstance(queryText, list) else queryText
    currentIntent = requestContent['queryResult']['intent']['displayName']
    logging.info(f"current Intent: {currentIntent}")
    params = requestContent['queryResult']['parameters']
    params["ip"] = requestContent["ip"]
    if currentIntent == "Order.drink":
        return await __handleOrderDrinkIntent(params, userMessage)
    elif currentIntent == "Order.pizza - drink no":
        params = menuHandler.params
        fullOrder = buildFullOrder(params)
        totalPriceDict = menuHandler.analyzeTotalPriceWithMenuPrices(fullOrder)
        finalMessage = totalPriceDict["finalMessage"]
        return sendWebhookCallback(finalMessage)
    elif currentIntent == "Order.pizza - drink yes":
        drinkString = menuHandler.getDrinksString()
        return sendWebhookCallback(drinkString)
    elif currentIntent == "Order.pizza":
        return __handleOrderPizzaIntent(queryText, requestContent)
    elif currentIntent == "Welcome":
        pizzaMenu = menuHandler.getPizzasString()
        welcomeString = f"Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n {pizzaMenu}." \
                        f" \nQual pizza você vai querer?"
        startContext = structureNewDialogflowContext(contextName="Start", lifespan=1)
        return sendWebhookCallback(botMessage=welcomeString, nextContext=startContext)
    return sendWebhookCallback(botMessage="a")


def __handleOrderPizzaIntent(queryText: str, requestContent: dict) -> Response:
    parameters = requestContent['queryResult']['parameters']
    fullPizza = parsePizzaOrder(userMessage=queryText, parameters=parameters)
    fullPizzaText = convertMultiplePizzaOrderToText(fullPizza)
    menuHandler.params["pizzas"].append(fullPizza)
    followUpContext = structureNewDialogflowContext("OrderPizza-followup")
    return sendWebhookCallback(botMessage=f"Maravilha! {fullPizzaText.capitalize()} então. "
                                          f"Você vai querer alguma bebida?", nextContext=followUpContext)


async def __handleOrderDrinkIntent(params: dict, userMessage: str) -> Response:
    ip_address = params["ip"]
    session = create_session(ip_address)
    drink = structureDrink(params, userMessage)
    menuHandler.params["drinks"].append(drink)
    parameters = menuHandler.params
    fullOrder = buildFullOrder(parameters)
    orderInfo = menuHandler.analyzeTotalPriceWithMenuPrices(fullOrder)
    finalMessage = orderInfo["finalMessage"]
    orderItems = orderInfo["orderItems"]
    totalPrice = orderInfo["totalPrice"]
    orderObject = format_order_data(order_items=orderItems, structured_order=fullOrder)
    session_metadata = session.metaData
    user = await get_all_users_from_global_object()
    finalOrderObject = build_socket_object(all_users=user, order_object=orderObject,
                                             session_metadata=session_metadata)
    finalOrderObject["totalPrice"] = totalPrice
    await send_message({'type': 'order', 'body': finalOrderObject})
    return sendWebhookCallback(finalMessage)


def __main():
    pass


if __name__ == "__main__":
    __main()
