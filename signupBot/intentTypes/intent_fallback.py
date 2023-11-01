from signupBot.intentTypes.base_intent import BaseIntent
from signupBot.intentTypes.replies import Replies, Types


class InstantFallbackIntent(BaseIntent):
    def getIntentType(self):
        return Types.INSTANT_FALLBACK

    def getChangeIntent(self):
        return self.reply["fallbackIntent"]

    def _produceFirstSentence(self):
        return self.reply["main"]

    def parseIncomingMessage(self, message: str):
        # sourcery skip: assign-if-exp, swap-if-expression
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()
        return {"changeIntent": "MENU", 'chosenOption': message}


def __main():
    fbi = InstantFallbackIntent(Replies.MENU)
    firstResponse = fbi.parseIncomingMessage("oii")
    firstResponse = fbi.parseIncomingMessage("eae")
    return


if __name__ == "__main__":
    __main()
