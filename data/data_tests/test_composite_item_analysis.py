import pytest

from data.speisekarte_extraction import analyzeCompositeItem


class TestCompositeItemAnalysis:
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

    def test_single_item(self, price_dict):
        desired_item = {'calabresa': 1.0}
        item_type = 'Pizza de'
        result = analyzeCompositeItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 17.5,
            'tag': '1 x Pizza de calabresa (R$17.50)'
        }

    def test_multiple_items(self, price_dict):
        desired_item = {'calabresa': 1.0, 'pepperoni': 2.0}
        item_type = 'Pizza de'
        result = analyzeCompositeItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 57.48,
            'tag': '1 x Pizza meio calabresa meio pepperoni (R$57.48)'
        }

    def test_zero_quantity(self, price_dict):
        desired_item = {'calabresa': 0.0, 'pepperoni': 0.0}
        item_type = 'Pizza de'
        result = analyzeCompositeItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 0.0,
            'tag': '1 x Pizza meio calabresa meio pepperoni (R$0.00)'
        }

    def test_nonexistent_item(self, price_dict):
        desired_item = {'nonexistent': 1.0}
        item_type = 'Pizza de'
        with pytest.raises(KeyError):
            analyzeCompositeItem(desired_item, price_dict, item_type)

    def test_integer_quantity(self, price_dict):
        desired_item = {'calabresa': 2}
        item_type = 'Pizza de'
        result = analyzeCompositeItem(desired_item, price_dict, item_type)
        assert result == {
            'price': 35.0,
            'tag': '1 x Pizza de calabresa (R$35.00)'
        }


if __name__ == "__main__":
    pytest.main()
