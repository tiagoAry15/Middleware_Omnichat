class Types:
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FALLBACK = "FALLBACK"
    ENTRY_TEXT = "ENTRY_TEXT"


class Replies:
    WELCOME = {"media": None,
               "intentName": "WELCOME",
               "intentType": Types.MULTIPLE_CHOICE,
               "main": "Olá! Bem-vindo à Pizza do Bill! O que você vai querer hoje?",
               "1": {"choiceContent": "Fazer um pedido", "choiceNextIntent": "FIRST_FLAVOR"},
               "2": {"choiceContent": "Ver o cardápio", "choiceNextIntent": "MENU"},
               "3": {"choiceContent": "Fazer cadastro", "choiceNextIntent": "SIGNUP_NAME"}}

    MENU = {"media": None,
            "intentName": "MENU",
            "intentType": Types.FALLBACK,
            "fallBackIntent": "WELCOME",
            "main": "Hoje temos Calabresa, Mussarela, Portuguesa e Margherita"}

    SIGNUP_NAME = {"media": None,
                   "intentName": "SIGNUP_NAME",
                   "intentType": Types.ENTRY_TEXT,
                   "nextIntent": "SIGNUP_EMAIL",
                   "main": "Qual o seu nome?",
                   "validators": ["name"]}

    SIGNUP_EMAIL = {"media": None,
                    "intentName": "SIGNUP_EMAIL",
                    "intentType": Types.ENTRY_TEXT,
                    "main": "Qual o seu email?",
                    "validators": ["email"]}

    DRINK = {"media": None,
             "intentName": "DRINK",
             "intentType": Types.MULTIPLE_CHOICE,
             "main": "Qual bebida você deseja?",
             "1": {"choiceContent": "Coca-cola", "choiceNextIntent": "FIRST_FLAVOR"},
             "2": {"choiceContent": "Fanta", "choiceNextIntent": "FIRST_FLAVOR"},
             "3": {"choiceContent": "Guaraná", "choiceNextIntent": "FIRST_FLAVOR"}}

    FIRST_FLAVOR = {"media": None,
                    "intentName": "FIRST_FLAVOR",
                    "intentType": Types.MULTIPLE_CHOICE,
                    "main": "Qual o primeiro sabor de pizza que você deseja?",
                    "1": {"choiceContent": "Calabresa", "choiceNextIntent": "SECOND_FLAVOR"},
                    "2": {"choiceContent": "Mussarela", "choiceNextIntent": "SECOND_FLAVOR"},
                    "3": {"choiceContent": "Portuguesa", "choiceNextIntent": "SECOND_FLAVOR"}}

    SECOND_FLAVOR = {"media": None,
                     "intentName": "SECOND_FLAVOR",
                     "intentType": Types.MULTIPLE_CHOICE,
                     "main": "Qual o segundo sabor de pizza que você deseja?",
                     "1": {"choiceContent": "Calabresa", "choiceNextIntent": None},
                     "2": {"choiceContent": "Mussarela", "choiceNextIntent": None},
                     "3": {"choiceContent": "Portuguesa", "choiceNextIntent": None}}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
