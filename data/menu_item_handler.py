from data.speisekarte_extraction import createMenuString, loadSpeisekarte, analyzeTotalPrice
from utils.decorators.singleton_decorator import singleton


@singleton
class MenuItemHandler:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPriceWithUpdatedPrices(self, structuredOrder: dict):
        return analyzeTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)


def __main():
    ds = MenuItemHandler()
    return


if __name__ == "__main__":
    __main()
