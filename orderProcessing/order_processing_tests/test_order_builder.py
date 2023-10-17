import pytest

from orderProcessing.order_builder import buildFullOrder
from orderProcessing.pizza_processor import _splitOrder, _translateOrder, parsePizzaOrder, __convertPizzaOrderToText


@pytest.mark.parametrize("parameters, expected_output", [
    (
            {'drinks': [{'suco de laranja': 2.0}],
             'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5},
                        {'calabresa': 0.5, 'pepperoni': 0.5}],
             'secret': 'Mensagem secreta'},
            {"Bebida": [{"suco de laranja": 2.0}], "Pizza": [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}
                , {"calabresa": 0.5, "pepperoni": 0.5}]}
    ),
    (
            {'pizzas': [{'calabresa': 1.0}]},
            {"Bebida": [], "Pizza": {'calabresa': 1.0}}
    ),
    (
            {'drinks': [{'água': 1.0}]},
            {"Bebida": [{"água": 1.0}], "Pizza": None}
    ),
    (
            {},
            {"Bebida": [], "Pizza": None}
    ),
])
def test_buildFullOrder(parameters, expected_output):
    output = buildFullOrder(parameters)
    assert output == expected_output


if __name__ == '__main__':
    pytest.main()
