from orderProcessing.drink_processor import structureDrink
from orderProcessing.order_builder import buildFullOrder
from orderProcessing.pizza_processor import parsePizzaOrder, convertMultiplePizzaOrderToText


def __testParsePizzaOrder():
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['inteira calabresa']}
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['meia calabresa meia calabresa']}
    # parameterInput = {'drinks': [], 'pizzas': ['meia calabresa meia pepperoni'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': [], 'pizzas': ['inteira frango'], 'secret': 'Mensagem secreta'}
    parameterInput = {'flavor': ['calabresa', 'margherita', 'queijo'], 'number': [1.0]}
    userMessage = 'vou querer duas calabresas e uma pizza meio margherita meio quatro queijos'
    output = parsePizzaOrder(userMessage, parameterInput)
    print(output)


def __testPizzaOrderToText():
    pizzaOrder = [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}]
    output = convertMultiplePizzaOrderToText(pizzaOrder)
    print(output)


def __testStructureDrink():
    userMessage = 'duas cocas e dois guaranás'
    parameters = {'Drinks': ['coca-cola', 'guaraná']}
    output = structureDrink(parameters, userMessage)
    print(output)


def __testConvertMultiplePizzaOrderToText():
    pizzaOrder = [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}, {'calabresa': 1.0}]
    output = convertMultiplePizzaOrderToText(pizzaOrder)
    print(output)


def __testBuildFullOrder():
    # orderTest = {'Bebida': [{'guaraná': 2.0}, {'suco de laranja': 1.0}],
    #              'Pizza': [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}, {'calabresa': 1.0}]}
    orderTest = {'drinks': [{"suco de laranja": 1.0}], 'pizzas': [[{'calabresa': 1.0}]], 'secret': 'Mensagem secreta'}
    output = buildFullOrder(orderTest)
    print(output)


def __main():
    output = convertMultiplePizzaOrderToText(orderList)
    # __testBuildFullOrder()
    # output = structureFullOrder(parameterInput)
    # output = parsePizzaOrder(
    #     "Vou querer duas pizzas de calabresa, uma meio pepperoni meio portuguesa e uma pizza meio calabresa meio "
    #     "pepperoni",
    #     {'flavor': ['calabresa', 'pepperoni', 'portuguesa']})
    # parameterInput = {'drinks': [{'guaraná': 1.0, 'suco de laranja': 2.0}],
    #                   'pizzas': [[{'calabresa': 2.0}, {'calabresa': 0.5, 'frango': 0.5}]],
    #                   'secret': 'Mensagem secreta'}
    # parameterInput = {'Drinks': ['suco de laranja', 'guaraná']}
    # output = structureDrink(parameters=parameterInput, userMessage="vou querer dois sucos de laranja e um guaraná")
    # print(output)
    return


if __name__ == '__main__':
    __main()
