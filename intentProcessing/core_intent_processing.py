import logging

from flask import request, Response

from api_config.object_factory import menuHandler
from intentProcessing.order_factory import format_order_data
from orderProcessing.drink_processor import structureDrink
from orderProcessing.order_builder import buildFullOrder
from orderProcessing.pizza_processor import parsePizzaOrder, convertMultiplePizzaOrderToText
from utils.dialogflow_utils import structureNewDialogflowContext
from utils.helper_utils import sendWebhookCallback


def fulfillment_processing(requestContent):
    print("FULFILLMENT ENDPOINT!")
    print(requestContent)
    outputContexts = requestContent['queryResult']['outputContexts']
    menuHandler.params["baseContextName"] = outputContexts[0]['name'].rsplit('/contexts/', 1)[0]
    queryText = requestContent['queryResult']['queryText']
    print("@@@ QUERY_TEXT → " + queryText)
    userMessage = [item["name"] for item in queryText] if isinstance(queryText, list) else queryText
    currentIntent = requestContent['queryResult']['intent']['displayName']
    logging.info(f"current Intent: {currentIntent}")
    params = requestContent['queryResult']['parameters']
    if currentIntent == "Order.drink":
        return __handleOrderDrinkIntent(params, userMessage)
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


def __handleOrderDrinkIntent(params: dict, userMessage: str) -> Response:
    drink = structureDrink(params, userMessage)
    menuHandler.params["drinks"].append(drink)
    parameters = menuHandler.params
    fullOrder = buildFullOrder(parameters)
    orderInfo = menuHandler.analyzeTotalPriceWithMenuPrices(fullOrder)
    finalMessage = orderInfo["finalMessage"]
    orderItems = orderInfo["orderItems"]
    totalPrice = orderInfo["totalPrice"]
    orderObject = format_order_data(orderItems, totalPrice)
    return sendWebhookCallback(finalMessage)
