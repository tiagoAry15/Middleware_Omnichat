class Types:
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    INSTANT_FALLBACK = "INSTANT_FALLBACK"
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
            "intentType": Types.INSTANT_FALLBACK,
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
                    "nextIntent": "SIGNUP_ADDRESS",
                    "main": "Qual o seu email?",
                    "validators": ["email"]}

    SIGNUP_ADDRESS = {"media": None,
                      "intentName": "SIGNUP_ADDRESS",
                      "intentType": Types.ENTRY_TEXT,
                      "nextIntent": "SIGNUP_BIRTHDATE",
                      "main": "Qual o seu endereço?",
                      "validators": ["address"]}

    SIGNUP_BIRTHDATE = {"media": None,
                        "intentName": "SIGNUP_BIRTHDATE",
                        "intentType": Types.ENTRY_TEXT,
                        "main": "Qual a sua data de nascimento?",
                        "validators": ["birthdate"]}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
