import pytest
from data.speisekarteExtraction import __createPizzaDescription, analyzeSingleItem, analyzeCompositeItem, \
    analyzeTotalPrice, loadSpeisekarte


def test_createPizzaDescription():
    testCases = [
        {
            'pizza_dict': {'calabresa': 0.5, 'margherita': 0.5},
            'expected_output': "Pizza meio calabresa meio margherita"
        },
        {
            'pizza_dict': {'calabresa': 0.5, 'margherita': 0.5, 'frango': 0.5},
            'expected_output': "Pizza meio calabresa e meio margherita e meio frango"
        }
    ]

    for data in testCases:
        pizza_dict = data['pizza_dict']
        expected_output = data['expected_output']
        assert __createPizzaDescription(pizza_dict) == expected_output


def test_analyzeSingleItem():
    testCases = [
        {
            'price_dict': {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99,
                           'Portuguesa': 13.99, 'Quatro Queijos': 16.9},
            'item': {'frango': 3.0},
            'item_type': 'Pizza de',
            'expected_output': {'price': 56.699999999999996, 'tag': '3 x Pizza de frango (R$56.70)'}
        }
    ]

    for data in testCases:
        price_dict = data['price_dict']
        item = data['item']
        item_type = data['item_type']
        expected_output = data['expected_output']
        assert analyzeSingleItem(item, price_dict, item_type) == expected_output


def test_analyzeCompositeItem():
    testCases = [
        {
            'price_dict': {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99,
                           'Portuguesa': 13.99, 'Quatro Queijos': 16.9},
            'item': {'calabresa': 0.5, 'margherita': 0.5},
            'item_type': 'Pizza',
            'expected_output': {'price': 16.5, 'tag': '1 x Pizza meio calabresa meio margherita (R$16.50)'}
        }
    ]

    for data in testCases:
        price_dict = data['price_dict']
        item = data['item']
        item_type = data['item_type']
        expected_output = data['expected_output']
        assert analyzeCompositeItem(item, price_dict, item_type) == expected_output


def test_analyzeTotalPrice():
    analyze_total_price_data = [
        {
            'menu': loadSpeisekarte(),
            'structured_order': {'Bebida': [{'guaraná': 2.0}], 'Pizza': [{'calabresa': 1.0}]},
            'expected_output': {
                "totalPrice": 27.48,
                "finalMessage": "Vai ser 1 x Pizza de calabresa (R$17.50),"
                                " 2 x Guaraná (R$9.98), totalizando R$27.48."
                                " Qual vai ser a forma de pagamento?"
                                " (pix/cartão/dinheiro)"
            }
        }
    ]

    for data in analyze_total_price_data:
        menu = data['menu']
        structured_order = data['structured_order']
        expected_output = data['expected_output']
        assert analyzeTotalPrice(structured_order, menu) == expected_output



if __name__ == "__main__":
    pytest.main()
