from typing import List


def __getDrinkPluralForm(drinks: List[str]) -> dict:
    # Add plural forms to drinks list and create a reverse map for later use
    drinks_plural = []
    reverse_map = {}
    for drink in drinks:
        words = drink.split()
        words[0] += 's'  # Add 's' to the first word
        plural_form = ' '.join(words)
        drinks_plural.append(plural_form)
        reverse_map[plural_form.replace(' ', '@')] = drink
        reverse_map[drink.replace(' ', '@')] = drink  # Include original drink name with spaces replaced by '@'
    drinks += drinks_plural
    return reverse_map


def structureDrink(parameters: dict, userMessage: str) -> dict:
    drinks = parameters.get('Drinks', [])
    numberEntity = {"uma": 1.0, "um": 1.0, "meio": 0.5, "meia": 0.5, "dois": 2.0, "duas": 2.0, "três": 3.0,
                    "quatro": 4.0}

    # Create a reverse map for later use
    reverseDrinkMap = __getDrinkPluralForm(drinks)

    # Step 1: replace spaces in composite drinks with "@"
    drinksReplaced = [drink.replace(' ', '@') for drink in drinks]

    # Step 2: replace drinks in the user message with the replaced versions
    for drink, drinkReplaced in zip(drinks, drinksReplaced):
        userMessage = userMessage.replace(drink, drinkReplaced)

    words = userMessage.split()
    drinkOrder = {
        word: numberEntity[words[i - 1]]
        for i, word in enumerate(words)
        if word in drinksReplaced and i > 0 and words[i - 1] in numberEntity
    }
    # Step 4: convert drink names back using the reverse_map
    for drinkReplaced in drinkOrder.copy():
        if drinkReplaced in reverseDrinkMap:
            originalDrinkName = reverseDrinkMap[drinkReplaced]
            drinkOrder[originalDrinkName] = drinkOrder.pop(drinkReplaced)

    return drinkOrder


def buildFullOrder(parameters: dict):
    """parameters example:  {'drinks': ['2 suco de laranja'],
                            'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5},
                             {'calabresa': 0.5, 'pepperoni': 0.5}],
                            'secret': 'Mensagem secreta'}"""
    drink = parameters["drinks"][0] if parameters.get("drinks") else None
    # Split drink into a list
    pizza = parameters["pizzas"][0]
    return {"Bebida": [{key: value} for key, value in drink.items()], "Pizza": pizza}


def _splitOrder(order: str) -> List[str]:
    order = order.replace('vou querer ', '')  # remove the starting phrase
    items = order.split(', ')  # split on comma

    # split items on ' e ' if ' e ' exists in items
    final_items = []
    for item in items:
        if ' e ' in item:
            subItems = item.split(' e ')
            final_items.extend(subItems)
        else:
            final_items.append(item)

    # re-add 'vou querer ' to the start of the first item
    final_items[0] = f'vou querer {final_items[0]}'
    return final_items

def __getQuantity(word: str, numberEntity: dict) -> float:
    return numberEntity.get(word)

def __getFlavor(word: str, availableFlavors: List[str], pluralFlavors: dict) -> str:
    correctWord = pluralFlavors.get(word, word)
    return correctWord if correctWord in availableFlavors else None

def _translateOrder(order: str, parameters: dict) -> dict:
    numberEntity = {"uma": 1.0, "meio": 0.5, "meia": 0.5, "duas": 2.0, "três": 3.0, "quatro": 4.0}
    availableFlavors = parameters['flavor']
    pluralFlavors = {f'{flavor}s': flavor for flavor in availableFlavors}
    result = {}
    words = order.split()
    current_number = None

    for word in words:
        quantity = __getQuantity(word, numberEntity)
        if quantity is not None:
            current_number = quantity
        else:
            flavor = __getFlavor(word, availableFlavors, pluralFlavors)
            if flavor is not None:
                if flavor not in result:
                    result[flavor] = 0
                result[flavor] += current_number or 1
    return result


def parsePizzaOrder(userMessage: str, parameters: dict) -> List[dict]:
    userMessage = userMessage.lower()
    individualOrders = _splitOrder(userMessage)
    pot = []
    for order in individualOrders:
        result = _translateOrder(order, parameters)
        pot.append(result)
    return pot


def __convertPizzaOrderToText(pizzaOrder: dict) -> str:
    result = []
    number_dict = {0.5: "meia", 1.0: "uma inteira", 2.0: "duas inteiras", 3.0: "três inteiras"}
    previous_order = None
    flavors = []

    for flavor, amount in pizzaOrder.items():
        if previous_order is None:
            previous_order = amount
        if previous_order != amount:
            order_text = f"{number_dict[previous_order]} {' '.join(flavors)}"
            result.append(order_text)
            flavors = []
        flavors.append(flavor)
        previous_order = amount

    if flavors:
        order_text = f"{number_dict[previous_order]} {' '.join(flavors)}"
        result.append(order_text)

    return ', '.join(result)



def convertMultiplePizzaOrderToText(pizzaOrders: List[dict]) -> str:
    result = []
    for pizzaOrder in pizzaOrders:
        order_text = __convertPizzaOrderToText(pizzaOrder)
        result.append(order_text)
    return ', '.join(result)


def __testParsePizzaOrder():
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['inteira calabresa'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['meia calabresa meia calabresa'], 'secret': 'Mensagem secreta'}
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
    userMessage = 'dois guaranás e um suco de laranja'
    parameters = {'Drinks': ['guaraná', 'suco de laranja']}
    output = structureDrink(parameters, userMessage)
    print(output)

def __testConvertMultiplePizzaOrderToText():
    pizzaOrder = [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}, {'calabresa': 1.0}]
    output = convertMultiplePizzaOrderToText(pizzaOrder)
    print(output)

def __testBuildFullOrder():
    orderTest = {'Bebida': [{'guaraná': 2.0}, {'suco de laranja': 1.0}],
                 'Pizza': [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}, {'calabresa': 1.0}]}
    output = buildFullOrder(orderTest)
    print(output)


def __main():
    __testBuildFullOrder()
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
