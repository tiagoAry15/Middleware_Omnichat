class Replies:
    WELCOME = {"media": None,
               "intent": "Welcome",
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": {"choiceContent": "Pedir uma pizza", "choiceNextIntent": "FIRST_FLAVOR"},
               "2": {"choiceContent": "Pedir uma bebida", "choiceNextIntent": None}}
    FIRST_FLAVOR = {"media": None,
                    "intent": "FIRST_FLAVOR",
                    "main": "Qual sabor de pizza você deseja?",
                    "1": {"choiceContent": "Calabresa", "choiceNextIntent": None},
                    "2": {"choiceContent": "Mussarela", "choiceNextIntent": None},
                    "3": {"choiceContent": "Portuguesa", "choiceNextIntent": None}}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
