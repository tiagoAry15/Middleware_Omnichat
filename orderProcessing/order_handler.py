from typing import List


def __extra_s_count(original: str, word: str) -> int:
    return word.count('s') - original.count('s')


def __get_plural_form(drink: str) -> str:
    words = drink.split()
    # Words which should not be pluralized
    skip_plural = ["de"]

    # Assuming plurals just add an 's' to the last word, except for words in skip_plural
    if len(words) > 1 and words[-2] not in skip_plural:
        words[-2] += 's'
    words[-1] += 's'

    return ' '.join(words)


def __getDrinkPluralForm(drinks: List[str]) -> dict:
    reverse_map = {}
    for drink in drinks:
        reverse_map[drink.replace(' ', '@')] = drink  # Singular form
        words = drink.split()

        # Handle plurals for last word
        words[-1] += 's'
        plural_drink_last = ' '.join(words)
        reverse_map[plural_drink_last.replace(' ', '@')] = drink

        # If the drink has multiple words, create more plural variations
        if len(words) > 1:
            # Only first word pluralized
            words[0] += 's'
            plural_drink_first = ' '.join(words)
            reverse_map[plural_drink_first.replace(' ', '@')] = drink

            # Remove the 's' added to the last word to get the sucos@de@laranja form
            words[-1] = words[-1][:-1]
            plural_drink_first_only = ' '.join(words)
            reverse_map[plural_drink_first_only.replace(' ', '@')] = drink

    return reverse_map


def __replaceDrinkSynonym(drinks: List[str], userMessage: str) -> str:
    replacedWords = set()  # Track words we've already replaced
    for drink in drinks:
        for word in userMessage.split():
            if word in replacedWords:
                continue
            if __extra_s_count(drink, word) > 0:
                userMessage = userMessage.replace(word, word.replace(' ', '@'))
                replacedWords.add(word)
            elif drink in word:
                userMessage = userMessage.replace(word, word.replace(' ', '@'))
                replacedWords.add(word)
    return userMessage


def structureDrink(parameters: dict, inputUserMessage: str) -> dict:
    drinks = parameters.get('Drinks', [])
    userMessage = __replaceDrinkSynonym(drinks, inputUserMessage)

    numberEntity = {
        "uma": 1.0, "um": 1.0, "meio": 0.5, "meia": 0.5,
        "dois": 2.0, "duas": 2.0, "três": 3.0, "quatro": 4.0
    }

    # Create a reverse map for later use
    reverseDrinkMap = __getDrinkPluralForm(drinks)
    drinkOrder = {}

    order = {}
    words = userMessage.split()
    for i, word in enumerate(words):
        if word in numberEntity:
            # Check if the next word(s) form a valid drink name
            for j in range(1, 5):  # Assume max length of drink name is 4 words
                potential_drink = '@'.join(words[i + 1:i + 1 + j])
                if potential_drink in reverseDrinkMap:
                    # Update the order with the identified drink and its number
                    order[reverseDrinkMap[potential_drink]] = numberEntity[word]
                    break

    return order


def buildFullOrder(parameters: dict):
    """parameters example:  {'drinks': ['2 suco de laranja'],
                            'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5},
                             {'calabresa': 0.5, 'pepperoni': 0.5}],
                            'secret': 'Mensagem secreta'}"""
    drink = parameters["drinks"][0] if parameters.get("drinks") and parameters["drinks"] else None
    pizza = parameters["pizzas"][0] if parameters.get("pizzas") and parameters["pizzas"] else None
    return {"Bebida": [{key: value} for key, value in (drink.items() if drink else [])], "Pizza": pizza}


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
    result1 = structureDrink({'Drinks': ['guaraná']}, 'vou querer um guaraná')
    result2 = structureDrink({'Drinks': ['guaraná']}, 'vou querer quatro guaranás')
    result3 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer um suco de laranja')
    result5 = structureDrink({'Drinks': ['guaraná', 'suco de laranja']},
                             'vou querer três guaranás e dois sucos de laranja')
    result4 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer dois sucos de laranja')
    orderList = [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}]
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
