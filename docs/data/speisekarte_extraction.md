## speisekarte_extraction.py

This module is responsible for handling the operations related to the "Speisekarte" (menu in German) of a pizza place. It includes functionalities to load the menu from a JSON file, create menu strings for display, and analyze the total price of an order. Here is a detailed breakdown of its functionalities:

### Imports:
- **json**: Used for loading the menu from a JSON file.
- **List**: Imported from the typing module to annotate the types of function parameters and return values.
- **getSpeisekartePath**: Imported from the references.path_reference module to get the path of the menu JSON file.

### Functions:
1. **loadSpeisekarte() -> dict**: Loads the menu from a JSON file and returns it as a dictionary.
2. **createMenuString(menu: dict, category: str = None) -> str**: Creates a string representation of a menu category (like pizzas or drinks) for display.
3. **__createPizzaDescription(pizza_dict: dict) -> str**: Creates a description string for a pizza item based on its toppings.
4. **analyzeSingleItem(desiredItem: dict, priceDict: dict, itemType: str) -> dict**: Analyzes a single item in the order and returns its details including a tag and the total price.
5. **analyzeCompositeItem(desiredItem: dict, priceDict: dict, itemType: str) -> dict**: Analyzes a composite item (like a pizza with multiple toppings) in the order and returns its details including a tag and the total price.
6. **__getItemDetails(item_type: str, desired_items: List[dict], price_dict: dict)**: Gets the details of all items in a particular category of the order.
7. **analyzeTotalPrice(structuredOrder: dict, menu: dict)**: Analyzes the total price of the order and constructs a final message including the order details and the total price.

### Main Function (__main__):
- Demonstrates the usage of the `__getItemDetails` function by calling it with example parameters and returning its output.

### JSON File (speisekarte.json):
- Contains the menu data including the names, sizes, and prices of pizzas and drinks, and the operating hours of the pizza place.

### Usage:
This module can be imported wherever menu handling functionalities are needed, especially in routes where orders are being processed and the total price is being calculated.

### load_speisekarte() example:
```python
menu = load_speisekarte()
```

```python
menu = {'Pizzas': [{'nome': 'Calabresa', 'tamanho': 'Grande', 'preço': 17.5}, {'nome': 'Frango', 'tamanho': 'Grande', 'preço': 18.9}, {'nome': 'Portuguesa', 'tamanho': 'Grande', 'preço': 13.99}, {'nome': 'Margherita', 'tamanho': 'Média', 'preço': 15.5}, {'nome': 'Quatro Queijos', 'tamanho': 'Grande', 'preço': 16.9}, {'nome': 'Pepperoni', 'tamanho': 'Grande', 'preço': 19.99}], 'Bebidas': [{'nome': 'Coca-cola', 'tamanho': '300ml', 'preço': 5.99}, {'nome': 'Guaraná', 'tamanho': '300ml', 'preço': 4.99}, {'nome': 'Suco de laranja', 'tamanho': '500ml', 'preço': 6.5}], 'HorárioDeFuncionamento': '17h às 22h'}
```

This line of code imports the menu from the JSON file and stores it in a variable called `menu`.

### createMenuString() example:
```python
menu = [{'nome': 'Calabresa', 'tamanho': 'Grande', 'preço': 17.5}, {'nome': 'Frango', 'tamanho': 'Grande', 'preço': 18.9}, {'nome': 'Portuguesa', 'tamanho': 'Grande', 'preço': 13.99}, {'nome': 'Margherita', 'tamanho': 'Média', 'preço': 15.5}, {'nome': 'Quatro Queijos', 'tamanho': 'Grande', 'preço': 16.9}, {'nome': 'Pepperoni', 'tamanho': 'Grande', 'preço': 19.99}]
category = 'pizzas'
menuString = createMenuString(menu, category)
```

```python
menuString = "Cardápio de pizzas:"
"- Calabresa - R$17.50"
"- Frango - R$18.90"
"- Portuguesa - R$13.99"
"- Margherita - R$15.50"
"- Quatro Queijos - R$16.90"
"- Pepperoni - R$19.99"
```

This line of code creates a menu string for pizzas and stores it in a variable called `menuString`.

### analyzeSingleItem() example:
```python
desiredItem = {'calabresa': 2.0}
priceDict = {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99, 'Portuguesa': 13.99,
                 'Quatro Queijos': 16.9}
itemType = 'Pizza de'
tag = analyzeSingleItem(desiredItem, priceDict, itemType)
```

```python
tag = {'price': 35.0, 'tag': '2 x Pizza de calabresa (R$35.00)'}
```

This line of code analyzes a single item in the order and stores its details in a variable called `tag`.

### analyzeCompositeItem() example:
```python
desiredItem = {'calabresa': 0.5, 'margherita': 0.5}
priceDict = {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99, 'Portuguesa': 13.99, 'Quatro Queijos': 16.9}
itemType = 'Pizza de'
tag = analyseCompositeItem(desiredItem, priceDict, itemType)
```

```python
tag = {'price': 16.5, 'tag': '1 x Pizza meio calabresa meio margherita (R$16.50)'}
```

This line of code analyzes a composite item in the order and stores its details in a variable called `tag`.

### analyzeTotalPrice() example:
```python
menu = {'Pizzas': [{'nome': 'Calabresa', 'tamanho': 'Grande', 'preço': 17.5}, {'nome': 'Frango', 'tamanho': 'Grande', 'preço': 18.9}, {'nome': 'Portuguesa', 'tamanho': 'Grande', 'preço': 13.99}, {'nome': 'Margherita', 'tamanho': 'Média', 'preço': 15.5}, {'nome': 'Quatro Queijos', 'tamanho': 'Grande', 'preço': 16.9}, {'nome': 'Pepperoni', 'tamanho': 'Grande', 'preço': 19.99}], 'Bebidas': [{'nome': 'Coca-cola', 'tamanho': '300ml', 'preço': 5.99}, {'nome': 'Guaraná', 'tamanho': '300ml', 'preço': 4.99}, {'nome': 'Suco de laranja', 'tamanho': '500ml', 'preço': 6.5}], 'HorárioDeFuncionamento': '17h às 22h'}
structuredOrder = {'Bebida': [{'guaraná': 1.0}, {'suco de laranja': 2.0}], 'Pizza': [{'calabresa': 0.5, 'margherita': 0.5}, {'frango': 1.0}]}
totalPriceDict = analyzeTotalPrice(structuredOrder, menu)
```

```python
totalPriceDict = {'totalPrice': 53.39, 'finalMessage': 'Vai ser 1 x Pizza meio calabresa meio margherita (R$16.50), 1 x Pizza de frango (R$18.90), 1 x Guaraná (R$4.99), 2 x Suco de laranja (R$13.00), totalizando R$53.39. Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)'}
```

This line of code analyzes the total price of the order and stores the details in a variable called `totalPriceDict`.