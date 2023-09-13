from typing import List


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


def __main():
    userMessage = "Vou querer uma de calabresa e uma meio portuguesa meio margherita"
    parameters = {'flavor': ['calabresa', 'portuguesa', 'margherita']}
    result = parsePizzaOrder(userMessage, parameters)
    orderText = convertMultiplePizzaOrderToText(result)
    print(result)


if __name__ == '__main__':
    __main()
