from orderProcessing.order_handler import structureDrink


class TestOrderHandlerDrink:
    def test_structureDrinkWithWordsAsQuantity(self):
        parameterInput = {'Drinks': ['suco de laranja', 'guaraná']}
        userMessage = 'vou querer dois sucos de laranja e um guaraná'
        expected_output = {'Drinks': [{'suco de laranja': 2.0}, {'guaraná': 1.0}]}
        assert structureDrink(parameterInput, userMessage) == expected_output

    def test_structureDrinkWithNumbersAsQuantity(self):
        parameterInput = {'Drinks': ['coca-cola', 'guaraná']}
        userMessage = 'vou querer 2 guaranás e 3 coca-colas'
        expected_output = {'Drinks': [{'guaraná': 2.0}, {'coca-cola': 3.0}]}
        assert structureDrink(parameterInput, userMessage) == expected_output

    def test_structureDrinkWithSynonyms(self):
        parameterInput = {'Drinks': ['coca-cola', 'guaraná']}
        userMessage = 'vou querer 2 cocas e 1 guarana'
        expected_output = {'Drinks': [{'coca-cola': 2.0}, {'guaraná': 1.0}]}
        assert structureDrink(parameterInput, userMessage) == expected_output

    def test_structureDrinkWithSynonymsAndWordsAsQuantity(self):
        parameterInput = {'Drinks': ['coca-cola', 'guaraná']}
        userMessage = 'duas coca e cinco suco de laranja'
        expected_output = {'Drinks': [{'coca-cola': 2.0}, {'suco de laranja': 5.0}]}
        assert structureDrink(parameterInput, userMessage) == expected_output
