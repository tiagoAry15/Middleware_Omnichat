from intentManipulation.replies import Replies, Types


class Intent:
    def __init__(self, coreReply: Replies):
        self.reply = coreReply
        self.coreMessage = coreReply["main"]
        self.intentType = coreReply["intentType"]
        self.alreadyWelcomed = False
        self.choice = 0

    def _formatOutputMessage(self, sentence: str = None):
        media = self.reply["media"]
        r = {"body": sentence}
        if media is not None:
            r["media"] = media
        return r

    def _produceFirstSentence(self):
        if self.reply["intentType"] == Types.MULTIPLE_CHOICE:
            text = self.reply["main"]
            choices = [value["choiceContent"] for key, value in self.reply.items() if key.isdigit()]
            menu = '\n'.join([f"{key}- {value}" for key, value in enumerate(choices, start=1)])
            return f"{text}\n{menu}"
        elif self.reply["intentType"] == Types.FALLBACK:
            return self.coreMessage

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


def __main():
    intent = Intent(Replies.WELCOME)
    botResponse = intent.parseIncomingMessage("oii")
    print(botResponse)
    return


if __name__ == "__main__":
    __main()
