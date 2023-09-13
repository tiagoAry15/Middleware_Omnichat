from colorama import Fore, Style

from utils.decorators.singleton_decorator import singleton
from firebaseFolder.firebase_user import FirebaseUser
from firebaseFolder.firebase_connection import FirebaseConnection
from intentManipulation.intentTypes.intent_entry_text import EntryTextIntent
from intentManipulation.intentTypes.intent_fallback import InstantFallbackIntent
from intentManipulation.intentTypes.replies import Replies


class IntentNotFoundException(Exception):
    def __init__(self, intent_name):
        self.intent_name = intent_name
        super().__init__(f"Intent '{intent_name}' not found.")


def getIntentPot():
    return [EntryTextIntent(Replies.SIGNUP_NAME), EntryTextIntent(Replies.SIGNUP_EMAIL),
            EntryTextIntent(Replies.SIGNUP_ADDRESS), EntryTextIntent(Replies.SIGNUP_CPF)]


@singleton
class IntentManager:
    def __init__(self):
        self.fc = FirebaseConnection()
        self.fu = FirebaseUser(self.fc)
        self.numberPot = []
        self.whatsappNumber = ""
        self.existingUser = False
        self.isUserChecked = False
        self.intents = getIntentPot()
        self.currentIntent = self.intents[0]
        self.extractedParameters = {}
        self.intentHistory = []  # Will store tuples (intent, messageContent)
        self.userHistory = []
        self.botHistory = []
        self.signupDetails = {}
        self.count = 0
        self.finished = False

    def __getIntentByName(self, inputIntentName: str):
        for intent in self.intents:
            currentName = intent.reply["intentName"].lower()
            check = isinstance(inputIntentName, str)
            if currentName == inputIntentName.lower():
                return intent
        raise IntentNotFoundException(inputIntentName)

    def _analyzeBotResponse(self, botResponse: dict):
        if self.isDefaultIntent(botResponse):
            botAnswer = botResponse["body"]
            self.botHistory.append(botAnswer)
        else:
            botAnswer = self.__handleIntentTransition(botResponse)
        self.intentHistory.append((self.currentIntent.reply["intentName"], botAnswer))
        return botAnswer

    def __handleIntentTransition(self, botResponse: dict):
        # sourcery skip: use-next
        nextIntentName = botResponse["changeIntent"]
        keyParameters = botResponse.get("parameters", {})
        action = botResponse.get("action")
        self._handleBotAction(action)
        self.extractedParameters.update(keyParameters)
        nextIntent = self.__getIntentByName(nextIntentName)
        nextIntentType = nextIntent.intentType
        if nextIntentType != "INSTANT_FALLBACK":
            self.currentIntent = nextIntent
        nextIntentAnswer = nextIntent.sendFirstMessage()["body"]

        if not isinstance(nextIntent, InstantFallbackIntent):
            self.botHistory.append(nextIntentAnswer)
            return nextIntentAnswer
        previousBotAnswer = ""
        for intentName, botAnswer in reversed(self.intentHistory):
            if intentName != nextIntentName:
                previousBotAnswer = botAnswer
                break
        finalAnswer = f"{nextIntentAnswer}\n\n{previousBotAnswer}"
        self.botHistory.append(nextIntentAnswer)
        return finalAnswer

    @staticmethod
    def isDefaultIntent(botResponse):
        return list(botResponse.keys()) == ["body"]

    def _handleBotAction(self, inputAction: str):
        if inputAction == "ASSEMBLY_SIGNUP":
            print("Cadastrando usuário...")
            self.signupDetails.update(self.extractedParameters)
            self.finished = True
            self.registerWhatsapp(self.signupDetails)

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        self.consoleLoop()

    def consoleLoop(self):
        while True:
            self.count += 1
            print(f"---- [{self.count}]")
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            self.userHistory.append(userMessage)
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            botAnswer = self._analyzeBotResponse(botResponse)
            if not self.finished:
                print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")
            print(f"                                  Parâmetros extraídos: {self.extractedParameters}\n")
            if self.finished:
                break

    def twilioSingleStep(self, userMessage: str):
        self.count += 1
        self.userHistory.append(userMessage)
        botResponse = self.currentIntent.parseIncomingMessage(userMessage)
        self.extractedParameters.update(botResponse.get("parameters", {}))
        action = botResponse.get("action")
        if action != "ASSEMBLY_SIGNUP":
            return self._analyzeBotResponse(botResponse)
        self.finished = True
        self.registerWhatsapp(self.extractedParameters)
        return "Usuário cadastrado com sucesso!"

    def existingWhatsapp(self, whatsappNumber: str) -> bool:
        return self.fu.existingUser({"phoneNumber": whatsappNumber})

    def registerWhatsapp(self, userDetails: dict):
        self.existingUser = True
        return self.fu.createUser(userDetails)

    def __checkUserExistence(self):
        if not self.isUserChecked:
            self.existingUser = self.existingWhatsapp(self.whatsappNumber)
            self.isUserChecked = True
        return self.existingUser

    def setWhatsappNumber(self, userNumber: str):
        self.whatsappNumber = userNumber
        self.__checkUserExistence()

    def needsToSignUp(self, userNumber: str):
        self.setWhatsappNumber(userNumber)
        return self.existingUser is False

    def handleIncomingMessage(self, message: str):
        return self.twilioSingleStep(message)


def __main():
    im = IntentManager()
    # existingUser = im.existingWhatsapp("+19574430239")
    existingUser = False
    if not existingUser:
        messagePot = ["Oii", "João", "Rua das Flores 4874", "19574430239"]
        lastBotAnswer = ""
        while lastBotAnswer != "Usuário cadastrado com sucesso!":
            newUserMessage = messagePot.pop(0)
            lastBotAnswer = im.twilioSingleStep(newUserMessage)
            print(f"User: {newUserMessage}")
            print(f"Bot: {lastBotAnswer}")
        return


if __name__ == "__main__":
    __main()
