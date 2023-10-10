import pytest

from orderProcessing.drink_processor import structureDrink


class TestStructureDrink:
    def test_single_simple_drink(self):
        drink_list = ["guaraná"]
        user_message = 'vou querer um guaraná'
        result = structureDrink(parameters={'Drinks': drink_list}, inputUserMessage=user_message)
        assert result == {"guaraná": 1.0}

    def test_multiple_simple_drinks(self):
        drink_list = ["guaraná"]
        user_message = 'vou querer quatro guaranás'
        result = structureDrink(parameters={'Drinks': drink_list}, inputUserMessage=user_message)
        assert result == {"guaraná": 4.0}

    def test_single_complex_drink(self):
        drink_list = ["suco de laranja"]
        user_message = 'vou querer um suco de laranja'
        result = structureDrink(parameters={'Drinks': drink_list}, inputUserMessage=user_message)
        assert result == {"suco de laranja": 1.0}

    def test_multiple_complex_drinks(self):
        drink_list = ["suco de laranja"]
        user_message = 'vou querer dois sucos de laranja'
        result = structureDrink(parameters={'Drinks': drink_list}, inputUserMessage=user_message)
        assert result == {"suco de laranja": 2.0}

    def test_mixed_drinks_order(self):
        drink_list = ["guaraná", "suco de laranja"]
        user_message = 'vou querer três guaranás e dois sucos de laranja'
        result = structureDrink(parameters={'Drinks': drink_list}, inputUserMessage=user_message)
        assert result == {"guaraná": 3.0, "suco de laranja": 2.0}


if __name__ == '__main__':
    pytest.main()
