from intentManipulation.intentTypes.replies import Replies


class FallbackIntent:
    def __init__(self, coreReply: Replies):
        if coreReply["intentType"].upper() != "FALLBACK":
            raise TypeError(f"FallbackIntent can only be instantiated with a Fallback. "
                            f"Got {coreReply['intentType']} instead.")
        self.reply = coreReply
        self.media = coreReply["media"]
        self.coreMessage = coreReply["main"]
        self.intentType = coreReply["intentType"]
        self.alreadyWelcomed = False

    def _formatOutputMessage(self, sentence: str = None):
        r = {"body": sentence}
        if self.media is not None:
            r["media"] = self.media
        return r

    def _produceFirstSentence(self):
        return self.reply["main"]

    def sendFirstMessage(self):
        self.alreadyWelcomed = True
        return self._formatOutputMessage(self._produceFirstSentence())

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()
        return {"changeIntent": Replies.MENU}


def __main():
    fbi = FallbackIntent(Replies.MENU)


if __name__ == "__main__":
    __main()
