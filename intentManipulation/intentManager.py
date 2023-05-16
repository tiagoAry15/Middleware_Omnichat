from typing import List

from intentManipulation.intent import Intent
from intentManipulation.replies import Replies


class IntentManager:
    def __init__(self, intents: List[Intent]):
        self.intents = intents

    def linkTwoIntents(self, incomingIntent: str, outgoingIntent: str):
        firstIntent: Intent = self.getIntentByName(incomingIntent)
        secondIntent: Intent = self.getIntentByName(outgoingIntent)
        firstIntent.setNextIntent(secondIntent)
        secondIntent.setPreviousIntent(firstIntent)

    def getIntentByName(self, inputIntentName: str) -> Intent or None:  # sourcery skip: use-next
        for intent in self.intents:
            currentName = intent.intentName.lower()
            if currentName == inputIntentName.lower():
                return intent
        return None


def __main():
    listOfIntents = [Intent(Replies.WELCOME), Intent(Replies.ORDER)]
    im = IntentManager(listOfIntents)
    im.linkTwoIntents("Welcome", "Order")
    return


if __name__ == "__main__":
    __main()
