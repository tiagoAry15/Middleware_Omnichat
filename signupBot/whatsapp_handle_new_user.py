from signupBot.intent_manager import IntentManager
import asyncio


async def handleNewWhatsappUser(metaData: dict):
    phoneNumber = metaData["phoneNumber"]
    userMessage = metaData["userMessage"]
    im = IntentManager()
    im.extractedParameters["phoneNumber"] = phoneNumber
    return await im.twilioSingleStep(userMessage)


async def user_creation_test():
    phoneNumber = "+558597648593"
    msgPool = ["Oi", "Ednaldo Pereira", "Rua da Paz 4987", "14568598577"]
    for msg in msgPool:
        msgWithMetaData = {"phoneNumber": phoneNumber, "userMessage": msg}
        botResponse = await handleNewWhatsappUser(msgWithMetaData)
        print(botResponse)
    return


async def __main():
    await user_creation_test()


if __name__ == "__main__":
    asyncio.run(__main())
