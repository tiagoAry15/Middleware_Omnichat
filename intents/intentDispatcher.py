from intents.replies import Replies


class Intent:
    def __init__(self, coreReply: Replies):
        self.reply = coreReply
        self.intentName = coreReply["intent"]
        self.coreMessage = coreReply["main"]
        self.choiceNumbers = [key for key in coreReply.keys() if key.isdigit()]

    def _formatOutputMessage(self, sentence: str = None):
        media = self.reply["media"]
        r = {"body": sentence}
        if media is not None:
            r["media"] = media
        return r

    def _produceFirstSentence(self):
        text = self.reply["main"]
        choices = [value for key, value in self.reply.items() if key.isdigit()]
        menu = '\n'.join([f"{key}-{value}" for key, value in enumerate(choices, start=1)])
        return f"{text}\n{menu}"

    def sendFirstMessage(self):
        firstSentence = self._produceFirstSentence()
        return self._formatOutputMessage(firstSentence)

    def handleIncomingMessage(self, message: str):
        if message not in self.choiceNumbers:
            return {"body": f"{message} não é uma opção. Por favor, selecione uma opção válida"}


def __main():
    intent = Intent(Replies.WELCOME)
    print(intent.sendFirstMessage())
    userMessage = "4"
    print(intent.handleIncomingMessage(userMessage))


if __name__ == "__main__":
    __main()
