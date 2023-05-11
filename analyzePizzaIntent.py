
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


def getRandomUserOrderExamples():
    pool = ["uma pizza de calabresa e outra meia queijo meio bacon",
            "uma calabresa uma mussarela",
            "uma pizza de calabresa e uma de mussarela",
            "meia frango catupiri meia calabresa",
            "uma pizza de calabresa e uma de mussarela"]
    return random.choice(pool)


def __main():
    randomOrder = getRandomUserOrderExamples()
    return


if __name__ == '__main__':
    __main()
