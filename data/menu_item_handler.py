from data.speisekarte_extraction import createMenuString, loadSpeisekarte, getTotalPrice, generateOrderFinalMessage
from utils.decorators.singleton_decorator import singleton


class MenuItemHandler:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPriceWithMenuPrices(self, structuredOrder: dict):
        totalPrice, orderItems = getTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)
        final_message = generateOrderFinalMessage(totalPrice=totalPrice, orderItems=orderItems)
        return {"totalPrice": totalPrice, "orderItems": orderItems, "finalMessage": final_message}


def __main():
    ds = MenuItemHandler()
    return


if __name__ == "__main__":
    __main()
