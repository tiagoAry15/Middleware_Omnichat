from typing import List

from colorama import Fore, Style

from firebaseFolder.FirebaseUser import FirebaseUser
from firebaseFolder.firebaseConnection import FirebaseConnection
from intentManipulation.intentTypes.intentEntryText import EntryTextIntent
from intentManipulation.intentTypes.intentFallback import InstantFallbackIntent
from intentManipulation.intentTypes.intentMultipleChoice import MultipleChoiceIntent
from intentManipulation.intentTypes.replies import Replies, Types


class IntentNotFoundException(Exception):
    def __init__(self, intent_name):
        self.intent_name = intent_name
        super().__init__(f"Intent '{intent_name}' not found.")


def getIntentPot():
    return [EntryTextIntent(Replies.SIGNUP_NAME), EntryTextIntent(Replies.SIGNUP_EMAIL),
            EntryTextIntent(Replies.SIGNUP_ADDRESS), EntryTextIntent(Replies.SIGNUP_CPF)]


class IntentManager:
    def __init__(self):
        self.fc = FirebaseConnection()
        self.fu = FirebaseUser(self.fc)
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
        action = botResponse.get("action")
        return self._analyzeBotResponse(botResponse) if action != "ASSEMBLY_SIGNUP" else\
            "Usuário cadastrado com sucesso!"

    def existingWhatsapp(self, whatsappNumber: str):
        return self.fu.existingUser({"phoneNumber": whatsappNumber})

    def registerWhatsapp(self, userDetails: dict):
        return self.fu.createUser(userDetails)


def __main():
    im = IntentManager()
    answers = []
    answers.append(im.twilioSingleStep("Oii"))
    print(answers[-1], im.extractedParameters)
    answers.append(im.twilioSingleStep("João"))
    print(answers[-1], im.extractedParameters)
    answers.append(im.twilioSingleStep("Rua das Flores 2542"))
    print(answers[-1], im.extractedParameters)
    answers.append(im.twilioSingleStep("19574430239"))
    print(answers[-1], im.extractedParameters)
    return


if __name__ == "__main__":
    __main()
