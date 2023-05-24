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


def __main():
    # parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['inteira calabresa'], 'secret': 'Mensagem secreta'}
    parameterInput = {'drinks': ['Um suco de laranja'], 'pizzas': ['meia calabresa meia calabresa'], 'secret': 'Mensagem secreta'}
    # parameterInput = {'drinks': [], 'pizzas': ['meia calabresa meia pepperoni'], 'secret': 'Mensagem secreta'}
    output = structureFullOrder(parameterInput)
    return


if __name__ == '__main__':
    __main()
