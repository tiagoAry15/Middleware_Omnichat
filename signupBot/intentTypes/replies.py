class Types:
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    INSTANT_FALLBACK = "INSTANT_FALLBACK"
    ENTRY_TEXT = "ENTRY_TEXT"


class Replies:
    WELCOME = {"media": None,
               "intentName": "WELCOME",
               "intentType": Types.MULTIPLE_CHOICE,
               "main": "Olá! Bem-vindo à Pizza do Bill! {'Cardápio'} {'Horários'}. O que você vai querer hoje?",
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
                   "main": "Parece que você não está cadastrado no nosso sistema, e vou precisar fazer o seu cadastro."
                           " Por favor, me informe o seu nome.",
                   "validators": ["name"],
                   "nextIntent": "SIGNUP_ADDRESS",}

    SIGNUP_EMAIL = {"media": None,
                    "intentName": "SIGNUP_EMAIL",
                    "intentType": Types.ENTRY_TEXT,
                    "main": "Qual o seu email?",
                    "validators": ["email"],
                    "nextIntent": "SIGNUP_ADDRESS"}

    SIGNUP_ADDRESS = {"media": None,
                      "intentName": "SIGNUP_ADDRESS",
                      "intentType": Types.ENTRY_TEXT,
                      "main": "Qual o seu endereço?",
                      "validators": ["address"],
                      "nextIntent": "SIGNUP_CPF"}

    SIGNUP_CPF = {"media": None,
                  "intentName": "SIGNUP_CPF",
                  "intentType": Types.ENTRY_TEXT,
                  "main": "Qual o seu CPF?",
                  "validators": ["cpf"],
                  "nextIntent": "SIGNUP_NAME"}

    SIGNUP_BIRTHDATE = {"media": None,
                        "intentName": "SIGNUP_BIRTHDATE",
                        "intentType": Types.ENTRY_TEXT,
                        "main": "Qual a sua data de nascimento?",
                        "validators": ["birthdate"],
                        "nextIntent": "SIGNUP_NAME"}


def __main():
    print(Replies.WELCOME)


if __name__ == "__main__":
    __main()
