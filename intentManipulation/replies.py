class Replies:
    WELCOME = {"media": None,
               "intent": "Welcome",
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": "Pedir uma pizza",
               "2": "Pedir uma bebida"}
    ORDER = {"media": None,
             "intent": "Order",
             "main": "Qual sabor de pizza você deseja?",
             "1": "Pepperoni",
             "2": "Margherita",
             "3": "Calabresa"}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
