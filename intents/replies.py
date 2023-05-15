class Replies:
    WELCOME = {"media": None,
               "intent": "Welcome",
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": "Pedir uma pizza",
               "2": "Pedir uma bebida"}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
