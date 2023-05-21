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
    drink = parameters["drinks"][0]
    pizza = parameters["pizzas"][0]
    fractionConverter = {"um": 1, "meia": 0.5, "inteira": 1}
    # Convert drink string to dict
    drink_quantity, drink_item = drink.split(' ', 1)
    drink_quantity = fractionConverter[drink_quantity.lower()]
    drink_dict = {"item": drink_item.capitalize(), "quantity": drink_quantity}

    # Convert pizza string to dict
    pizza_quantity, pizza_item = pizza.split(' ', 1)
    pizza_quantity = fractionConverter[pizza_quantity.lower()]
    pizza_dict = {"item": f"pizza de {pizza_item}".capitalize(), "quantity": pizza_quantity}

    return {"drink": drink_dict, "pizza": pizza_dict}


def __main():
    parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['inteira calabresa'], 'secret': 'Mensagem secreta'}
    output = structureFullOrder(parameterInput)
    return


if __name__ == '__main__':
    __main()
