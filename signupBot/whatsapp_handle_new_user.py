from signupBot.intent_manager import IntentManager


def handleNewWhatsappUser(phoneNumber: str, receivedMessage: str):
    im = IntentManager()
    im.extractedParameters["phoneNumber"] = phoneNumber
    return im.twilioSingleStep(receivedMessage)


def user_creation_test():
    phoneNumber = "+558597648593"
    msgPool = ["Oi", "Ednaldo Pereira", "Rua da Paz 4987", "14568598577"]
    for msg in msgPool:
        botResponse = handleNewWhatsappUser(phoneNumber, msg)
        print(botResponse)
    return


def __main():
    user_creation_test()


if __name__ == "__main__":
    __main()
