import json
from typing import List

from references.pathReference import getSpeisekartePath


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
        size = item['tamanho']

        itemString = f"- {name} ({size}) - R${price:.2f}\n"
        menuString += itemString

    return menuString


def __getItemDetails(item_type: str, desired_items: List[dict], price_dict: dict):
    order_items = []
    if not desired_items or (len(desired_items) == 1 and not desired_items[0]):
        return order_items
    if not isinstance(desired_items, list):
        desired_items = [desired_items]
    if desired_items:
        for item in desired_items:
            # item is a single dict like {'guaraná': 1.0}
            item_name = list(item.keys())[0].capitalize()
            item_quantity = item[item_name.lower()]
            item_price = price_dict[item_name]
            adjusted_price = item_price * item_quantity
            item_tag = f"{item_quantity} x {item_type} {item_name} (R${adjusted_price:.2f})"
            total_price = item_price * item_quantity
            order_items.append({"tag": item_tag, "price": total_price})
    return order_items


def analyzeTotalPrice(structuredOrder: dict, menu: dict):
    # Convert menu lists to dictionaries for easier access
    dictDrinkLabeledPrices = {item["nome"]: item["preço"] for item in menu["Bebidas"]}
    dictPizzaLabeledPrices = {item["nome"]: item["preço"] for item in menu["Pizzas"]}

    # Get the order details
    desiredDrinks = structuredOrder.get("Bebida")
    desiredPizzas = structuredOrder.get("Pizza")

    # Get item details
    orderItems = __getItemDetails('', desiredDrinks, dictDrinkLabeledPrices)
    orderItems += __getItemDetails('Pizza de', desiredPizzas, dictPizzaLabeledPrices)

    # Calculate the total price
    totalPrice = sum(item["price"] for item in orderItems)
    orderTags = [item["tag"] for item in orderItems]

    # Construct the final message
    finalMessage = f"Vai ser {', '.join(orderTags)}, totalizando R${totalPrice:.2f}." \
                   f" Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)"

    return {"totalPrice": totalPrice, "finalMessage": finalMessage}


def __main():
    speisekarte = loadSpeisekarte()
    # structuredOrderExample = {'Bebida': {'item': 'Suco de laranja', 'quantity': 1}, 'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    # structuredOrderExample = {'Bebida': {}, 'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    # structuredOrderExample = {'Bebida': [{'item': 'Suco de laranja', 'quantity': 1}],
    #                           'Pizza': [{'item': 'Calabresa', 'quantity': 0.5},
    #                                     {'item': 'Pepperoni', 'quantity': 0.5}]}
    structuredOrderExample = {'Bebida': [{'guaraná': 1.0}, {'suco de laranja': 2.0}],
                              'Pizza': [{'calabresa': 2.0}, {'calabresa': 0.5, 'frango': 0.5}]}
    price = analyzeTotalPrice(structuredOrderExample, speisekarte)
    print(price)
    return


if __name__ == '__main__':
    __main()
