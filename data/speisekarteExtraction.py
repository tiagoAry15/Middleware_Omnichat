import json

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


def analyzeTotalPrice(structuredOrder: dict, menu: dict):
    # Convert menu lists to dictionaries for easier access
    dictDrinkLabeledPrices = {item["nome"]: item["preço"] for item in menu["Bebidas"]}
    dictPizzaLabeledPrices = {item["nome"]: item["preço"] for item in menu["Pizzas"]}

    # Get the order details
    desiredDrinks = structuredOrder.get("Bebida")
    desiredPizzas = structuredOrder.get("Pizza")

    # Initialize variables
    desiredDrinkPrice, desiredDrinkName, desiredDrinkAmount = (0, ) * 3
    desiredPizzaPrice, desiredPizzaName, desiredPizzaAmount = (0, ) * 3
    orderItems = []

    # If there are drinks in the order, get their details
    if desiredDrinks:
        desiredDrinkName = desiredDrinks["item"]
        desiredDrinkAmount = desiredDrinks["quantity"]
        desiredDrinkPrice = dictDrinkLabeledPrices[desiredDrinkName]
        orderItems.append(f"{desiredDrinkAmount} x {desiredDrinkName} (R${desiredDrinkPrice:.2f})")

    # If there are pizzas in the order, get their details
    if desiredPizzas:
        desiredPizzaName = desiredPizzas["item"]
        desiredPizzaAmount = desiredPizzas["quantity"]
        desiredPizzaPrice = dictPizzaLabeledPrices[desiredPizzaName]
        orderItems.append(f"{desiredPizzaAmount} x {desiredPizzaName} (R${desiredPizzaPrice:.2f})")

    # Calculate the total price
    totalPrice = desiredDrinkPrice * desiredDrinkAmount + desiredPizzaPrice * desiredPizzaAmount

    # Construct the final message
    finalMessage = f"Vai ser {', '.join(orderItems)}, totalizando R${totalPrice:.2f}." \
                   f" Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)"

    return {"totalPrice": totalPrice, "finalMessage": finalMessage}



def __main():
    speisekarte = loadSpeisekarte()
    # structuredOrderExample = {'Bebida': {'item': 'Suco de laranja', 'quantity': 1}, 'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    structuredOrderExample = {'Bebida': {}, 'Pizza': {'item': 'Calabresa', 'quantity': 1}}
    price = analyzeTotalPrice(structuredOrderExample, speisekarte)
    print(price)
    return


if __name__ == '__main__':
    __main()
