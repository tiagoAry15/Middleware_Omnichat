from signupBot.intentTypes.base_intent import BaseIntent
from signupBot.intentTypes.replies import Replies, Types


class MultipleChoiceIntent(BaseIntent):
    def __init__(self, coreReply: Replies):
        super().__init__(coreReply)

    def getIntentType(self):
        return Types.MULTIPLE_CHOICE

    def _produceFirstSentence(self):
        text = self.reply["main"]
        choices = [value["choiceContent"] for key, value in self.reply.items() if key.isdigit()]
        menu = '\n'.join([f"{key}- {value}" for key, value in enumerate(choices, start=1)])
        return f"{text}\n{menu}"

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()
        choice = int(message)
        integerChoices = [int(key) for key in self.reply.keys() if key.isdigit()]
        if choice not in integerChoices:
            return {"body": f"[{message}] não é uma opção válida. "
                            f"Por favor, selecione uma opção entre {integerChoices}"}
        choiceReply = self.reply[message]
        newIntent = choiceReply["choiceNextIntent"]
        return {"changeIntent": newIntent, "chosenOption": choice,
                "chosenOptionDetails": choiceReply["choiceContent"]}


def __main():
    mci = MultipleChoiceIntent(Replies.WELCOME)
    firstResponse = mci.parseIncomingMessage("oii")
    print(firstResponse)
    print(mci.parseIncomingMessage("1"))


if __name__ == "__main__":
    __main()
