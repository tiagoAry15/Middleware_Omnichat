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


def getParameterExamples():
    parameterPot = [{"input": "vou querer uma pizza de calabresa",
                     "output": {'flavor': ['calabresa'], 'number': [1.0]}},
                    {"input": "vou querer uma pizza meia calabresa meia frango",
                     "output": {'flavor': ['calabresa', 'frango'], 'number': [0.5, 0.5]}}]


def __main():
    return


if __name__ == '__main__':
    __main()
