## _order_builder.py_

This module is responsible for constructing a full order based on the provided parameters, which include details about drinks and pizzas. Here are the functionalities provided by this module:

- **buildFullOrder(parameters: dict)**: This function takes a dictionary with details about drinks and pizzas as input and constructs a full order. The input dictionary should follow the structure shown in the function's docstring. The function returns a dictionary with the first drink and the first pizza from the input dictionary.

- **__getBuildFullOrderInputExample()**: This function returns an example input dictionary that can be used to test the `buildFullOrder` function.

- **__main()**: This function demonstrates how to use the `buildFullOrder` function by calling it with the example input dictionary returned by `__getBuildFullOrderInputExample`.

### Usage

This module is used to build a full order from a dictionary containing details about drinks and pizzas. It can be used to quickly construct an order for testing or other purposes.

### Examples

```python
fullOrderInput = __getBuildFullOrderInputExample()
fullOrderResult = buildFullOrder(fullOrderInput)
print(fullOrderResult)  # Output: {'Bebida': [{'suco de laranja': 2.0}], 'Pizza': {'calabresa': 2.0}}
```

### Results

```python
fullOrderInput = {'drinks': [{'suco de laranja': 2.0}], 'pizzas': [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}], 'secret': 'Mensagem secreta'}
fullOrderResult = {'Bebida': [{'suco de laranja': 2.0}], 'Pizza': {'calabresa': 2.0}}
````