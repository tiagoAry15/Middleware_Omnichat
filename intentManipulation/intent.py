from intentManipulation.replies import Replies


class Intent:
    def __init__(self, coreReply: Replies):
        self.reply = coreReply
        self.intentName = coreReply["intent"]
        self.coreMessage = coreReply["main"]
        self.choiceNumbers = [key for key in coreReply.keys() if key.isdigit()]
        self.alreadyWelcomed = False
        self.nextIntent: Replies = None
        self.previousIntent: Replies = None
        self.choice = 0

    def _formatOutputMessage(self, sentence: str = None):
        media = self.reply["media"]
        r = {"body": sentence}
        if media is not None:
            r["media"] = media
        return r

    def _produceFirstSentence(self):
        text = self.reply["main"]
        choices = [value["choiceContent"] for key, value in self.reply.items() if key.isdigit()]
        menu = '\n'.join([f"{key}- {value}" for key, value in enumerate(choices, start=1)])
        return f"{text}\n{menu}"

    def sendFirstMessage(self):
        self.alreadyWelcomed = True
        firstSentence = self._produceFirstSentence()
        return self._formatOutputMessage(firstSentence)

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
        return {"changeIntent": newIntent}

    def setNextIntent(self, newIntent):
        self.nextIntent = newIntent

    def setPreviousIntent(self, newIntent):
        self.previousIntent = newIntent


def __main():
    intent = Intent(Replies.FIRST_FLAVOR)
    return
    # print(intent.sendFirstMessage())
    # userMessage = "4aaaaa"
    # print(intent.parseIncomingMessage(userMessage))


if __name__ == "__main__":
    __main()
