## _pizza_processor.py_

This module is responsible for processing pizza orders from user messages. It contains several functions that help in parsing, translating, and converting pizza orders from the input messages. Here are the functionalities provided by this module:

- **_splitOrder(order: str) -> List[str]**: This function splits the user's message into individual orders. It first removes the phrase "vou querer" from the start, then splits the message based on commas and the word "e".

- **__getQuantity(word: str, numberEntity: dict) -> float**: This function takes a word and a dictionary of number entities as inputs and returns the corresponding quantity as a float.

- **__getFlavor(word: str, availableFlavors: List[str], pluralFlavors: dict) -> str**: This function takes a word, a list of available flavors, and a dictionary of plural flavors as inputs, and returns the singular form of the flavor if it is available.

- **_translateOrder(order: str, parameters: dict) -> dict**: This function translates an individual order into a dictionary with flavors as keys and quantities as values. It uses the `__getQuantity` and `__getFlavor` functions to parse the order.

- **parsePizzaOrder(userMessage: str, parameters: dict) -> List[dict]**: This function takes the user message and parameters as inputs and returns a list of dictionaries representing the parsed pizza orders. It uses the `_splitOrder` and `_translateOrder` functions to parse the message.

- **__convertPizzaOrderToText(pizzaOrder: dict) -> str**: This function takes a dictionary representing a pizza order and converts it into a human-readable string.

- **convertMultiplePizzaOrderToText(pizzaOrders: List[dict]) -> str**: This function takes a list of dictionaries representing multiple pizza orders and converts them into a human-readable string.

### Usage

This module is used to process user messages to identify and structure pizza orders. It can handle messages with different phrasing and plural forms of pizza names.

### Examples

```python
userMessage = "Vou querer uma de calabresa e uma meio portuguesa meio margherita"
parameters = {'flavor': ['calabresa', 'portuguesa', 'margherita']}
parsedOrder = parsePizzaOrder(userMessage, parameters)
order_text = convertMultiplePizzaOrderToText(parsedOrder)
print(order_text)
````

### Results
```python
parsedOrder = [{'calabresa': 1.0}, {'portuguesa': 0.5, 'margherita': 0.5}]
order_text = 'uma inteira calabresa, meia portuguesa margherita'
````
