from signupBot.intent_manager import IntentManager


def handleNewWhatsappUser(metaData: dict):
    phoneNumber = metaData["phoneNumber"]
    userMessage = metaData["userMessage"]
    im = IntentManager()
    im.extractedParameters["phoneNumber"] = phoneNumber
    return im.twilioSingleStep(userMessage)


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
