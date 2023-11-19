import os

from signupBot.intent_manager import SignupBot
import asyncio


async def handleNewWhatsappUser(userMessage: str, phoneNumber: str, signupBotInstance: SignupBot):
    signupBotInstance.extractedParameters["phoneNumber"] = phoneNumber
    return await signupBotInstance.twilioSingleStep(userMessage)


async def user_creation_test():
    phoneNumber = "+558597648593"
    msgPool = ["Oi", "Ednaldo Pereira", "Rua da Paz 4987", "14568598577"]
    for msg in msgPool:
        msgWithMetaData = {"phoneNumber": phoneNumber, "userMessage": msg}
        botResponse = await handleNewWhatsappUser(msgWithMetaData)
        print(botResponse)
    return


def __main():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(user_creation_test())
    finally:
        loop.close()


if __name__ == "__main__":
    __main()

