from intentManipulation.intentTypes.replies import Replies


class BaseIntent:
    def __init__(self, coreReply: Replies):
        if coreReply["intentType"] != self.getIntentType():
            raise TypeError(f"{self.__class__.__name__} can only be instantiated with a {self.getIntentType()}. "
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

    def sendFirstMessage(self):
        self.alreadyWelcomed = True
        return self._formatOutputMessage(self._produceFirstSentence())

    def parseIncomingMessage(self, message: str):
        raise NotImplementedError("Subclasses must implement parseIncomingMessage method.")

    def _parse_message(self, message: str):
        raise NotImplementedError("Subclasses must implement _parse_message method.")

    def _produceFirstSentence(self):
        raise NotImplementedError("Subclasses must implement produceFirstSentence method.")

    def getIntentType(self):
        raise NotImplementedError("Subclasses must implement getIntentType method.")

    def getChangeIntent(self):
        raise NotImplementedError("Subclasses must implement getChangeIntent method.")
