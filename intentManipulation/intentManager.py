from typing import List

from colorama import Fore, Style

from intentManipulation.intentTypes.intentEntryText import EntryTextIntent
from intentManipulation.intentTypes.intentFallback import InstantFallbackIntent
from intentManipulation.intentTypes.intentMultipleChoice import MultipleChoiceIntent
from intentManipulation.intentTypes.replies import Replies, Types


class IntentNotFoundException(Exception):
    def __init__(self, intent_name):
        self.intent_name = intent_name
        super().__init__(f"Intent '{intent_name}' not found.")


def getIntentPot():
    return [MultipleChoiceIntent(Replies.WELCOME), InstantFallbackIntent(Replies.MENU),
            EntryTextIntent(Replies.SIGNUP_NAME), EntryTextIntent(Replies.SIGNUP_EMAIL),
            EntryTextIntent(Replies.SIGNUP_ADDRESS), EntryTextIntent(Replies.SIGNUP_BIRTHDATE)]


class IntentManager:
    def __init__(self, intents: List):
        self.intents = intents
        self.currentIntent = intents[0]
        self.extractedParameters = {}
        self.intentHistory = []  # Will store tuples (intent, messageContent)
        self.userHistory = []
        self.botHistory = []
        self.signupDetails = {}
        self.count = 0

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
        print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")

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

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        while True:
            self.count += 1
            print(f"---- [{self.count}]")
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            self.userHistory.append(userMessage)
            # print(f"Intent → {self.currentIntent.reply['intentName']}")
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            self._analyzeBotResponse(botResponse)
            print(f"                                  Parâmetros extraídos: {self.extractedParameters}\n")


def __main():
    listOfIntents = getIntentPot()
    im = IntentManager(listOfIntents)
    im.chatBotLoop()
    d1 = {"action": "get", "items": [{"itemType": "pizza", "itemFlavor": "calabresa", "itemSize": "grande",
                                      "itemQuantity": 1},
                                     {"itemType": "pizza", "itemFlavor": "mussarela", "itemSize": "grande",
                                      "itemQuantity": 1}]}
    return


if __name__ == "__main__":
    __main()
