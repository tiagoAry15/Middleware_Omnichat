# Order Handler

The `Order Handler` module, implemented in `orderHandler.py`, contains several functions aimed at handling and processing orders, particularly for pizzas and drinks.

## Table of Contents
- [Functions](#functions)
  - [structureDrink](#structureDrink)
  - [buildFullOrder](#buildFullOrder)
  - [parsePizzaOrder](#parsePizzaOrder)
  - [convertMultiplePizzaOrderToText](#convertMultiplePizzaOrderToText)
- [Test](#test)


<a name="functions"></a>
## Functions

<a name="structureDrink"></a>
### structureDrink

### `structureDrink(parameters: dict, inputUserMessage: str) -> dict`

This function structures a drink order by matching drinks in the user's message and mapping them to quantities.

#### structureDrink Input example
```python
parameters = {'Drinks': ['guaraná', 'coca-cola']}
aux = structureDrink(parameters, "vou querer dois guaranás e uma coca")
print(aux)
```

#### structureDrink Output example
``` python
{'coca-cola': 1, 'guaraná': 2}
```


<a name="buildFullOrder"></a>
### buildFullOrder
### `buildFullOrder(parameters: dict)`

This function structures the full order, including both drinks and pizzas, into a dictionary.

#### buildFullOrder Input example
```python
parameters = {'drinks': [{"suco de laranja": 1.0}], 'pizzas': [[{'calabresa': 1.0}]], 'secret': 'Mensagem secreta'}
aux = buildFullOrder(parameters, "vou querer dois guaranás e uma coca")
print(aux)
```

#### buildFullOrder Output example
```python
{'Bebida': [{'suco de laranja': 1.0}], 'Pizza': [{'calabresa': 1.0}]}
```


<a name="parsePizzaOrder"></a>
### parsePizzaOrder
### `parsePizzaOrder(userMessage: str, parameters: dict) -> List[dict]`

This function parses the user's pizza order into structured data.

#### parsePizzaOrder Input example
```python
userMessage = "Vou querer duas pizzas de calabresa, uma meio pepperoni meio portuguesa e uma pizza meio calabresa meio pepperoni" 
parameters = {'flavor': ['calabresa', 'pepperoni', 'portuguesa']}
aux = parsePizzaOrder(userMessage, parameters)
print(aux)
```

#### _parsePizzaOrder Output example
``` python
[{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}]
```

<a name="convertMultiplePizzaOrderToText"></a>
### convertMultiplePizzaOrderToText
### `convertMultiplePizzaOrderToText(pizzaOrders: List[dict]) -> str`

This function takes multiple pizza orders and converts them to a readable string.

#### convertMultiplePizzaOrderToText Input example
```python
orderList = orderList = [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}]
aux = convertMultiplePizzaOrderToText(orderList)
print(aux)
```

#### convertMultiplePizzaOrderToText Output example
``` python
"duas inteiras calabresa, meia pepperoni portuguesa, meia calabresa pepperoni"
```

<a name="test"></a>
### Test
The accompanying test file (test_orderHandler.py) contains test cases for several of these functions using the pytest framework. To execute the tests, simply run the test file with pytest.

```python
if __name__ == '__main__':
    pytest.main()
```