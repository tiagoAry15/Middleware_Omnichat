import json
from typing import List

from references.path_reference import getSpeisekartePath


def loadSpeisekarte() -> dict:
    path = getSpeisekartePath()
    with path.open(encoding='utf-8') as file:
        return json.load(file)


def createMenuString(menu: dict, category: str = None) -> str:
    if category is None:
        raise ValueError("Category cannot be None")
    menuString = f"Cardápio de {category}:\n"

    for item in menu:
        name = item['nome']
        price = item['preço']

        itemString = f"- {name} - R${price:.2f}\n"
        menuString += itemString

    return menuString


def _createPizzaDescription(pizza_dict: dict) -> str:
    toppings = list(pizza_dict.keys())
    if len(toppings) == 1:
        return f"Pizza de {toppings[0]}"
    elif len(toppings) == 2:
        return f"Pizza meio {toppings[0]} meio {toppings[1]}"
    else:
        meio_toppings = [f"meio {topping}" for topping in toppings]
        return "Pizza " + " e ".join(meio_toppings)


def analyzeSingleItem(desiredItem: dict, priceDict: dict, itemType: str) -> dict:
    itemName = list(desiredItem.keys())[0].capitalize()
    itemQuantity = desiredItem[itemName.lower()]
    if itemQuantity.is_integer():
        itemQuantity = int(itemQuantity)
    itemPrice = priceDict[itemName]
    adjustedPrice = itemPrice * itemQuantity
    if itemType == 'Pizza de':
        fullTag = _createPizzaDescription(desiredItem)
        itemTag = f"{itemQuantity} x {fullTag} (R${adjustedPrice:.2f})"
    else:
        itemTag = f"{itemQuantity} x {itemName} (R${adjustedPrice:.2f})"
    total_price = itemPrice * itemQuantity
    return {"tag": itemTag, "price": total_price}


def analyzeCompositeItem(desiredItem: dict, priceDict: dict, itemType: str) -> dict:
    itemNames = [i.capitalize() for i in list(desiredItem.keys())]
    itemQuantities = [desiredItem[i.lower()] for i in itemNames]
    itemPrices = [priceDict[i] for i in itemNames]
    adjustedPrice = sum(i * j for i, j in zip(itemQuantities, itemPrices))
    fullTag = _createPizzaDescription(desiredItem)
    itemTag = f"1 x {fullTag} (R${adjustedPrice:.2f})"
    return {"tag": itemTag, "price": adjustedPrice}


def __getItemDetails(item_type: str, desired_items: List[dict], price_dict: dict):
    order_items = []
    if not desired_items or (len(desired_items) == 1 and not desired_items[0]):
        return order_items
    if not isinstance(desired_items, list):
        desired_items: List[dict] = [desired_items]
    if desired_items:
        for item in desired_items:
            if len(item) == 1:
                tag = analyzeSingleItem(desiredItem=item, priceDict=price_dict, itemType=item_type)
            else:
                tag = analyzeCompositeItem(desiredItem=item, priceDict=price_dict, itemType=item_type)
            order_items.append(tag)
    return order_items


def getTotalPrice(structuredOrder: dict, menu: dict):
    # Convert menu lists to dictionaries for easier access
    dictDrinkLabeledPrices = {item["nome"]: item["preço"] for item in menu["Bebidas"]}
    dictPizzaLabeledPrices = {item["nome"]: item["preço"] for item in menu["Pizzas"]}

    # Get the order details
    desiredDrinks = structuredOrder.get("Bebida")
    desiredPizzas = structuredOrder.get("Pizza")

    # Get item details
    orderItems = __getItemDetails('Pizza de', desiredPizzas, dictPizzaLabeledPrices)
    orderItems += __getItemDetails('', desiredDrinks, dictDrinkLabeledPrices)

    # Calculate the total price
    totalPrice = sum(item["price"] for item in orderItems)

    return totalPrice, orderItems


def generateOrderFinalMessage(totalPrice: float, orderItems: list) -> str:
    orderTags = [item["tag"] for item in orderItems]
    mergedItems = '\n- '.join(orderTags)

    finalMessage = f"Vai ser: \n- {mergedItems} \n- Total → [R${totalPrice:.2f}]\n" \
                   f" Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)"

    return finalMessage


def __main():
    speisekarte = loadSpeisekarte()
    # desiredItem = {'calabresa': 2.0}
    # priceDict = {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99, 'Portuguesa': 13.99,
    #              'Quatro Queijos': 16.9}
    # itemType = 'Pizza de'
    # tag = analyzeSingleItem(desiredItem, priceDict, itemType)
    structuredOrderExample = {'Bebida': {'item': 'Suco de laranja', 'quantity': 1},
                              'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    structuredOrderExample = {'Bebida': {}, 'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    structuredOrderExample = {'Bebida': [{'item': 'Suco de laranja', 'quantity': 1}],
                              'Pizza': [{'item': 'Calabresa', 'quantity': 0.5},
                                        {'item': 'Pepperoni', 'quantity': 0.5}]}
    structuredOrderExample = {'Bebida': [{'guaraná': 2.0}, {'suco de laranja': 1.0}],
                              'Pizza': [{'calabresa': 0.5, 'margherita': 0.5}, {'frango': 3.0}, {'calabresa': 2.0}]}
    # output = analyzeTotalPrice(structuredOrderExample, speisekarte)
    # finalMessage = output["finalMessage"]
    # price = output["totalPrice"]
    # item_type = "Pizza de"
    # desired_items = [{'calabresa': 0.5, 'mussarela': 0.5}, {'frango': 1.0}]
    # price_dict = {'Calabresa': 17.5, 'Frango': 18.9, 'Margherita': 15.5, 'Pepperoni': 19.99, 'Portuguesa': 13.99,
    #               'Quatro Queijos': 16.9}
    # return __getItemDetails(item_type, desired_items, price_dict)
    # print(output["finalMessage"])
    return


if __name__ == '__main__':
    __main()
