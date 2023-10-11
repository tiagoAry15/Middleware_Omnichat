from data.speisekarte_extraction import loadSpeisekarte, createMenuString, analyzeTotalPrice
from dialogflowFolder.dialogflow_session import DialogflowSession
from utils.decorators.singleton_decorator import singleton


@singleton
class DialogFlowHandler:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}
        self.session_instance = DialogflowSession()

    def requestDialogflowResponse(self, message: str):
        return self.session_instance.getDialogFlowResponse(message=message)

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPrice(self, structuredOrder: dict):
        return analyzeTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)


def __main():
    ds = DialogFlowHandler()
    return


if __name__ == "__main__":
    __main()
