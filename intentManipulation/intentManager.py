from typing import List

from colorama import Fore, Style

from intentManipulation.intentTypes.intentEntryText import EntryTextIntent
from intentManipulation.intentTypes.intentFallback import InstantFallbackIntent
from intentManipulation.intentTypes.intentMultipleChoice import MultipleChoiceIntent
from intentManipulation.intentTypes.replies import Replies, Types


def getIntentPot():
    return [MultipleChoiceIntent(Replies.WELCOME), InstantFallbackIntent(Replies.MENU),
            EntryTextIntent(Replies.SIGNUP)]


class IntentManager:
    def __init__(self, intents: List):
        self.intents = intents
        self.currentIntent = intents[0]
        self.intentHistory = []  # Will store tuples (intent, messageContent)
        self.count = 0

    def __getIntentByName(self, inputIntentName: str):
        for intent in self.intents:
            currentName = intent.reply["intentName"].lower()
            if currentName == inputIntentName.lower():
                return intent
        return None

    def _analyzeBotResponse(self, botResponse: dict):
        if self.isDefaultIntent(botResponse):
            botAnswer = botResponse["body"]
        else:
            botAnswer = self.__handleIntentTransition(botResponse)
        # store intent name along with its message in the history
        self.intentHistory.append((self.currentIntent.reply["intentName"], botAnswer))
        print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")

    def __handleIntentTransition(self, botResponse: dict):
        # sourcery skip: use-next
        nextIntentName = botResponse["changeIntent"]
        nextIntent = self.__getIntentByName(nextIntentName)
        self.currentIntent = nextIntent
        nextIntentAnswer = nextIntent.sendFirstMessage()["body"]

        if not isinstance(nextIntent, InstantFallbackIntent):
            return nextIntentAnswer
        previousBotAnswer = ""
        for intentName, botAnswer in reversed(self.intentHistory):
            if intentName != nextIntentName:
                previousBotAnswer = botAnswer
                break
        return f"{nextIntentAnswer}\n\n{previousBotAnswer}"

    @staticmethod
    def isDefaultIntent(botResponse):
        return list(botResponse.keys()) == ["body"]

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        while True:
            self.count += 1
            print(f"-------------- [{self.count}]")
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            self._analyzeBotResponse(botResponse)


def __main():
    listOfIntents = getIntentPot()
    im = IntentManager(listOfIntents)
    im.chatBotLoop()
    return


if __name__ == "__main__":
    __main()
