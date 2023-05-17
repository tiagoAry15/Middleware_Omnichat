from typing import List

from colorama import Fore, Style

from intentManipulation.intent import Intent
from intentManipulation.replies import Replies, Types


class IntentManager:
    def __init__(self, intents: List[Intent]):
        self.intents = intents
        self.currentIntent = intents[0]

    def __getIntentByName(self, inputIntentName: str) -> Intent or None:  # sourcery skip: use-next
        for intent in self.intents:
            currentName = intent.reply["intentName"].lower()
            if currentName == inputIntentName.lower():
                return intent
        return None

    def _analyzeBotResponse(self, botResponse: dict):
        botAnswer = self.handleIntentChanges(botResponse)
        print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")

    def handleIntentChanges(self, botResponse):
        if "changeIntent" not in botResponse:
            return botResponse["body"]
        nextIntent = botResponse["changeIntent"]
        newIntentObject: Intent = self.__getIntentByName(nextIntent)
        isNextIntentFallback = newIntentObject.intentType == Types.FALLBACK
        if isNextIntentFallback:
            return newIntentObject.sendFirstMessage()["body"]
        if newIntentObject is None:
            raise ValueError(f"Intent {nextIntent} not found.")
        self.currentIntent = newIntentObject
        return self.currentIntent.sendFirstMessage()["body"]

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        while True:
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            self._analyzeBotResponse(botResponse)


def __main():
    listOfIntents = [Intent(Replies.WELCOME), Intent(Replies.DRINK), Intent(Replies.FIRST_FLAVOR),
                     Intent(Replies.SECOND_FLAVOR), Intent(Replies.MENU)]
    im = IntentManager(listOfIntents)
    im.chatBotLoop()
    return


if __name__ == "__main__":
    __main()
