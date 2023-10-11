from data.speisekarte_extraction import loadSpeisekarte, createMenuString, analyzeTotalPrice


class SpeisekarteObject:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPrice(self, structuredOrder: dict):
        return analyzeTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)


def __main():
    so = SpeisekarteObject()
    print(so.speisekarte)


if __name__ == "__main__":
    __main()
