def buildFullOrder(parameters: dict):
    """parameters example:  {'drinks': {'suco de laranja': 2.0},
                            'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5},
                             {'calabresa': 0.5, 'pepperoni': 0.5}],
                            'secret': 'Mensagem secreta'}"""
    drink = parameters["drinks"][0] if parameters.get("drinks") and parameters["drinks"] else None
    pizza = parameters["pizzas"][0] if parameters.get("pizzas") and parameters["pizzas"] else None
    return {"Bebida": [{key: value} for key, value in (drink.items() if drink else [])], "Pizza": pizza}


def __getBuildFullOrderInputExample():
    return {'drinks': [{'suco de laranja': 2.0}],
            'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5},
                       {'calabresa': 0.5, 'pepperoni': 0.5}],
            'secret': 'Mensagem secreta'}


def __main():
    fullOrderInput = __getBuildFullOrderInputExample()
    fullOrderResult = buildFullOrder(fullOrderInput)
    return


if __name__ == '__main__':
    __main()
