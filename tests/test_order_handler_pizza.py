from orderProcessing.pizza_processor import parsePizzaOrder


class TestOrderHandlerPizza:
    def test_parsePizzaOnePizzaOneFlavor(self):
        parameterInput = {'flavor': ['calabresa']}
        userMessage = 'vou querer uma calabresa'
        expected_output = [{'calabresa': 1.0}]
        assert parsePizzaOrder(userMessage, parameterInput) == expected_output

    def test_parsePizzaOnePizzaTwoFlavors(self):
        parameterInput = {'flavor': ['calabresa', 'margherita']}
        userMessage = 'vou querer uma calabresa e uma margherita'
        expected_output = [{'calabresa': 1.0}, {'margherita': 1.0}]
        assert parsePizzaOrder(userMessage, parameterInput) == expected_output

    def test_parsePizzaOrderTwoPizzasThreeFlavors(self):
        parameterInput = {'flavor': ['calabresa', 'margherita', 'quatro queijos']}
        userMessage = 'vou querer duas calabresas e uma pizza meio margherita meio quatro queijos'
        expected_output = [{'calabresa': 2.0}, {'margherita': 0.5, 'queijo': 0.5}]
        assert parsePizzaOrder(userMessage, parameterInput) == expected_output

    def test_parsePizzaOrderWithNumbersAsQuantity(self):
        parameterInput = {'flavor': ['calabresa', 'margherita', 'frango']}
        userMessage = 'vou querer 2 de frango e 1 pizza meio margherita meio calabresa'
        expected_output = [{'frango': 2.0}, {'margherita': 0.5, 'queijo': 0.5}]
        assert parsePizzaOrder(userMessage, parameterInput) == expected_output
