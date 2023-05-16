from typing import List

from colorama import Fore, Style

from intentManipulation.intent import Intent
from intentManipulation.replies import Replies


class IntentManager:
    def __init__(self, intents: List[Intent]):
        self.intents = intents
        self.currentIntent = intents[0]

    def __getIntentByName(self, inputIntentName: str) -> Intent or None:  # sourcery skip: use-next
        for intent in self.intents:
            currentName = intent.intentName.lower()
            if currentName == inputIntentName.lower():
                return intent
        return None

    def _analyzeBotResponse(self, botResponse: dict):
        botAnswer = ""
        if "changeIntent" in botResponse:
            newIntentName = botResponse["changeIntent"]
            newIntentObject = self.__getIntentByName(newIntentName)
            if newIntentObject is None:
                raise ValueError(f"Intent {newIntentName} not found.")
            self.currentIntent = newIntentObject
            botAnswer = self.currentIntent.sendFirstMessage()["body"]
        else:
            botAnswer = botResponse["body"]
        print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        while True:
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            self._analyzeBotResponse(botResponse)


def __main():
    listOfIntents = [Intent(Replies.WELCOME), Intent(Replies.FIRST_FLAVOR)]
    im = IntentManager(listOfIntents)
    im.chatBotLoop()
    return


if __name__ == "__main__":
    __main()
