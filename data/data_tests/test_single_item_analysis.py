import pytest

from data.speisekarte_extraction import analyzeSingleItem


class TestSingleItemAnalysis:
    @pytest.fixture
    def price_dict(self):
        return {
            'Calabresa': 17.5,
            'Frango': 18.9,
            'Margherita': 15.5,
            'Pepperoni': 19.99,
            'Portuguesa': 13.99,
            'Quatro Queijos': 16.9
        }

    def test_pizza_type(self, price_dict):
        desired_item = {'calabresa': 2.0}
        item_type = 'Pizza de'
        result = analyzeSingleItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 35.0,
            'tag': '2 x Pizza de calabresa (R$35.00)'
        }

    def test_non_pizza_type(self, price_dict):
        desired_item = {'calabresa': 3.0}
        item_type = 'Item de'
        result = analyzeSingleItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 52.5,
            'tag': '3 x Calabresa (R$52.50)'
        }

    def test_single_quantity(self, price_dict):
        desired_item = {'pepperoni': 1.0}
        item_type = 'Pizza de'
        result = analyzeSingleItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 19.99,
            'tag': '1 x Pizza de pepperoni (R$19.99)'
        }

    def test_nonexistent_item(self, price_dict):
        desired_item = {'nonexistent': 1.0}
        item_type = 'Pizza de'
        with pytest.raises(KeyError):
            analyzeSingleItem(desired_item, price_dict, item_type)

    def test_zero_quantity(self, price_dict):
        desired_item = {'calabresa': 0.0}
        item_type = 'Pizza de'
        result = analyzeSingleItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 0.0,
            'tag': '0 x Pizza de calabresa (R$0.00)'
        }


if __name__ == "__main__":
    pytest.main()
