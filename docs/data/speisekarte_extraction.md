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

### Example:
```python
from speisekarte_extraction import loadSpeisekarte, createMenuString, analyzeTotalPrice
```

This line of code imports the necessary functions from the speisekarte_extraction.py module, ready to be used in other parts of the application for menu handling tasks.