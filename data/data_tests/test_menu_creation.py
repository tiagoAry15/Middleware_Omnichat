import pytest

from data.speisekarte_extraction import loadSpeisekarte, createMenuString, _createPizzaDescription

menu = loadSpeisekarte()


class TestMenuCreation:
    def test_create_menu_string(self):
        category = "Pizzas"
        submenu = menu[category]
        result = createMenuString(menu=submenu, category=category).replace("\n", "")
        assert "Cardápio de Pizzas:" in result


class TestPizzaDescription:
    def test_single_topping_pizza(self):
        pizza_dict = {'calabresa': 2.0}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza de calabresa"
        assert result == expected_result

    def test_two_topping_pizza(self):
        pizza_dict = {'mushroom': 1.5, 'pepperoni': 2.0}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza meio mushroom meio pepperoni"
        assert result == expected_result

    def test_three_or_more_topping_pizza(self):
        pizza_dict = {'onion': 1.0, 'green pepper': 1.0, 'olives': 1.0}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza meio onion e meio green pepper e meio olives"
        assert result == expected_result

    def test_empty_pizza(self):
        pizza_dict = {}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza "
        assert result == expected_result

    def test_additional_toppings(self):
        pizza_dict = {'ham': 2.5, 'cheese': 1.0, 'pineapple': 1.5, 'mushroom': 1.0}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza meio ham e meio cheese e meio pineapple e meio mushroom"
        assert result == expected_result

    def test_duplicate_toppings(self):
        pizza_dict = {'pepperoni': 2.0, 'pepperoni': 2.0}
        result = _createPizzaDescription(pizza_dict)
        expected_result = "Pizza de pepperoni"
        assert result == expected_result


if __name__ == "__main__":
    pytest.main()
