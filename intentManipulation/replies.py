class Replies:
    WELCOME = {"media": None,
               "intentName": "WELCOME",
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": {"choiceContent": "Pedir uma pizza", "choiceNextIntent": "FIRST_FLAVOR"},
               "2": {"choiceContent": "Pedir uma bebida", "choiceNextIntent": "DRINK"}}

    DRINK = {"media": None,
             "intentName": "DRINK",
             "main": "Qual bebida você deseja?",
             "1": {"choiceContent": "Coca-cola", "choiceNextIntent": "FIRST_FLAVOR"},
             "2": {"choiceContent": "Fanta", "choiceNextIntent": "FIRST_FLAVOR"},
             "3": {"choiceContent": "Guaraná", "choiceNextIntent": "FIRST_FLAVOR"}}

    FIRST_FLAVOR = {"media": None,
                    "intentName": "FIRST_FLAVOR",
                    "main": "Qual o primeiro sabor de pizza que você deseja?",
                    "1": {"choiceContent": "Calabresa", "choiceNextIntent": None},
                    "2": {"choiceContent": "Mussarela", "choiceNextIntent": None},
                    "3": {"choiceContent": "Portuguesa", "choiceNextIntent": None}}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
