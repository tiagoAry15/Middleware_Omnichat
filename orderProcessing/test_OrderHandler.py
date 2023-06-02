import pytest

from orderProcessing.orderHandler import (structureDrink, structureFullOrder, _splitOrder, _translateOrder,
                                          parsePizzaOrder, __convertPizzaOrderToText
                                          )


@pytest.mark.parametrize("userMessage, parameters, expected_output", [
    (
            "Vou querer uma pizza de calabresa",
            {'flavor': ['calabresa']},
            [{'calabresa': 1.0}]
    ),
    (
            "Vou querer duas pizzas de calabresa, uma meio pepperoni meio portuguesa "
            "e uma pizza meio calabresa meio pepperoni",
            {'flavor': ['calabresa', 'pepperoni', 'portuguesa']},
            [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}]
    ),
    (
            "Quero uma pizza de queijo",
            {'flavor': ['queijo']},
            [{'queijo': 1.0}]
    ),
    (
            "Vou querer uma pizza meio calabresa meio margherita",
            {'flavor': ['calabresa', 'margherita']},
            [{'calabresa': 0.5, 'margherita': 0.5}]
    ),
])
def test_parsePizzaOrder(userMessage, parameters, expected_output):
    output = parsePizzaOrder(userMessage, parameters)
    assert output == expected_output


@pytest.mark.parametrize("parameters, expected_output", [
    ({"number": 1, "Drinks": "Coca"}, "Um Coca"),
    ({"number": 2, "Drinks": "Pepsi"}, "2 Pepsi"),
    ({"number": 3, "Drinks": "Fanta"}, "3 Fanta"),
    ({"number": 4, "Drinks": "Sprite"}, "4 Sprite"),
    # more test cases...
])
def test_structureDrink(parameters, expected_output):
    assert structureDrink(parameters) == expected_output


if __name__ == '__main__':
    pytest.main()
