class Replies:
    WELCOME = {"media": None,
               "intent": "Welcome",
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": "Pedir uma pizza",
               "2": "Pedir uma bebida"}
    TWILIO = ("https://www.twilio.com/pt-br/", None)
    DEFAULT = ("Olá, eu me chamo Quizy e sou um bot de quiz.", None)


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
