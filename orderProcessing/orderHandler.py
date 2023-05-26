import re
from typing import List


def structurePizza(parameters: dict):
    flavors = parameters.get('flavor', [])
    numbers = parameters.get('number', [])
    formatted_flavors = []
    for flavor, number in zip(flavors, numbers):
        if number == 1 or number <= 0 or number >= 1:
            formatted_flavors.append(f'inteira {flavor}')
        else:
            formatted_flavors.append(f"meia {flavor}")
    return " ".join(formatted_flavors)


def structureDrink(parameters: dict):
    number = int(parameters.get('number', []))
    drink = parameters.get('Drinks', [])
    drink_string = 'um' if number == 1 else f'{number}'
    return f'{drink_string.capitalize()} {drink}'


def structureFullOrder(parameters: dict):
    drink = parameters["drinks"][0] if parameters.get("drinks") else None
    pizza = parameters["pizzas"][0]
    fractionConverter = {"um": 1, "meia": 0.5, "inteira": 1}

    if drink is not None:
        # Convert drink string to dict
        drink_quantity, drink_item = drink.split(' ', 1)
        drink_quantity = fractionConverter[drink_quantity.lower()]
        drink_dict = {"item": drink_item.capitalize(), "quantity": drink_quantity}
    else:
        drink_dict = {}

    # Convert pizza string to list of dicts
    pizza_parts = pizza.split(' ')
    pizza_dicts = []
    for i in range(0, len(pizza_parts), 2):
        pizza_quantity = fractionConverter[pizza_parts[i].lower()]
        pizza_item = pizza_parts[i + 1]
        pizza_dict = {"item": f"{pizza_item}".capitalize(), "quantity": pizza_quantity}
        pizza_dicts.append(pizza_dict)

    return {"Bebida": [drink_dict], "Pizza": pizza_dicts}


def __splitOrder(order: str) -> List[str]:
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


def __translateOrder(order: str, parameters: dict) -> dict:
    numberEntity = {"uma": 1.0, "meio": 0.5, "meia": 0.5, "duas": 2.0, "três": 3.0, "quatro": 4.0}

    # Initialize an empty result dictionary
    result = {}

    # Split the order into words
    words = order.split()

    # Initialize current number to None
    current_number = None

    # Iterate over each word in the order
    for word in words:
        # If the word is a number, update current number
        if word in numberEntity:
            current_number = numberEntity[word]
        elif word in parameters['flavor']:
            if current_number is None:
                raise ValueError(f"No quantity specified for flavor '{word}'.")
            if word in result:
                result[word] += current_number
            else:
                result[word] = current_number
            # Reset current number if it's not 1.0 (as it's for "meio"/"meia")
            if current_number != 1.0:
                current_number = None
    return result


def parsePizzaOrder(userMessage: str, parameters: dict):
    userMessage = userMessage.lower()
    individualOrders = __splitOrder(userMessage)
    return [__translateOrder(order, parameters) for order in individualOrders]


def __main():
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['inteira calabresa'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['meia calabresa meia calabresa'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': [], 'pizzas': ['meia calabresa meia pepperoni'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': [], 'pizzas': ['inteira frango'], 'secret': 'Mensagem secreta'}
    # output = structureFullOrder(parameterInput)
    output = parsePizzaOrder(
        "Vou querer duas pizzas de calabresa, uma meio pepperoni meio portuguesa e uma pizza meio calabresa meio "
        "pepperoni",
        {'flavor': ['calabresa', 'pepperoni', 'portuguesa']})
    print(output)
    return output


if __name__ == '__main__':
    __main()
