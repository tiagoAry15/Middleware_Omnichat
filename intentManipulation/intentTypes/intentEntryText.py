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
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.match(pattern, email)

    @staticmethod
    def _validateName(name: str):
        pattern = r'\b[A-Za-z._%+-]+\b'
        return re.match(pattern, name)

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()

        validators = self.reply["validators"] if self.reply["validators"] is not None else []
        if "name" in validators:
            validName = self._validateName(message)
            if not validName:
                return {"body": f'"{message}" não é um nome válido. Por favor, insira um nome válido.'}
        if "email" in validators:
            validEmail = self._validateEmail(message)
            if not validEmail:
                return {"body": f'"{message}" não é um email válido. Por favor, insira um e-mail válido.'}

        return {"changeIntent": self.reply["nextIntent"], "name": message}


def __main():
    eti = EntryTextIntent(Replies.SIGNUP_NAME)
    firstResponse = eti.parseIncomingMessage("oii")
    print(firstResponse)
    secondResponse = eti.parseIncomingMessage("Ronald")
    print(secondResponse)


if __name__ == "__main__":
    __main()
