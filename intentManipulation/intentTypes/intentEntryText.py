import re

from intentManipulation.intentTypes.baseIntent import BaseIntent
from intentManipulation.intentTypes.replies import Replies, Types


class EntryTextIntent(BaseIntent):
    def __init__(self, coreReply: Replies):
        super().__init__(coreReply)

    def getIntentType(self):
        return Types.ENTRY_TEXT

    def _produceFirstSentence(self):
        return self.reply["main"]

    @staticmethod
    def _validateEmail(email: str):
        # Email regex pattern
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.match(pattern, email)

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()

        validators = self.reply["validators"] if self.reply["validators"] is not None else []
        if "email" in validators:
            validEmail = self._validateEmail(message)
            if not validEmail:
                return {"body": "Por favor, insira um e-mail válido."}

        return {"changeIntent": self.reply["nextIntent"], "name": message}


def __main():
    eti = EntryTextIntent(Replies.SIGNUP)
    print(eti.parseIncomingMessage("oii"))
    print(eti.parseIncomingMessage("1"))


if __name__ == "__main__":
    __main()
