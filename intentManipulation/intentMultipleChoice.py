from intentManipulation.replies import Replies, Types


class MultipleChoiceIntent:
    def __init__(self, coreReply: Replies):
        if coreReply["intentType"] != Types.MULTIPLE_CHOICE:
            raise TypeError(f"MultipleChoiceIntent can only be instantiated with a MultipleChoiceIntent. "
                            f"Got {coreReply['intentType']} instead.")
        self.reply = coreReply
        self.media = coreReply["media"]
        self.coreMessage = coreReply["main"]
        self.intentType = coreReply["intentType"]
        self.alreadyWelcomed = False
        self.choice = 0

    def _formatOutputMessage(self, sentence: str = None):
        r = {"body": sentence}
        if self.media is not None:
            r["media"] = self.media
        return r

    def _produceFirstSentence(self):
        text = self.reply["main"]
        choices = [value["choiceContent"] for key, value in self.reply.items() if key.isdigit()]
        menu = '\n'.join([f"{key}- {value}" for key, value in enumerate(choices, start=1)])
        return f"{text}\n{menu}"

    def sendFirstMessage(self):
        self.alreadyWelcomed = True
        return self._formatOutputMessage(self._produceFirstSentence())

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()
        self.choice = int(message)
        integerChoices = [int(key) for key in self.reply.keys() if key.isdigit()]
        if self.choice not in integerChoices:
            return {"body": f"[{message}] não é uma opção válida. "
                            f"Por favor, selecione uma opção entre {integerChoices}"}
        choiceReply = self.reply[message]
        newIntent = choiceReply["choiceNextIntent"]
        return {"changeIntent": newIntent, "chosenOption": self.choice,
                "chosenOptionDetails": choiceReply["choiceContent"]}


def __main():
    mci = MultipleChoiceIntent(Replies.MENU)
    print(mci.parseIncomingMessage("oii"))
    print(mci.parseIncomingMessage("1"))


if __name__ == "__main__":
    __main()
