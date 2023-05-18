import re

from intentManipulation.intentTypes.baseIntent import BaseIntent
from intentManipulation.intentTypes.replies import Replies, Types


class EntryTextIntent(BaseIntent):
    """Full Name, Email, Delivery Address, Birthdate, Phone Number, CEP, etc."""

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
        pattern = r'\b[A-Za-záàâãéèêíïóôõöúçñ._%+-]+\b'
        return re.match(pattern, name)

    @staticmethod
    def _validateAddress(name: str):
        pattern = r'^(Rua|Avenida|Travessa)\s[^\d]*\d+$'
        match = re.match(pattern, name)

        if not match:
            if not re.match(r'^(Rua|Avenida|Travessa)', name):
                return "Tipo de endereço inválido (rua, avenida, travessa)"
            elif not re.search(r'\d', name):
                return "Endereço inválido. Está faltando o número da casa."
            else:
                return False

    @staticmethod
    def _validateBirthdate(birthdate: str):
        pattern = r'\b\d{2}\/\d{2}\/\d{4}\b'
        return re.match(pattern, birthdate)

    def parseIncomingMessage(self, message: str):
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()

        validators = self.reply["validators"] if self.reply["validators"] is not None else []
        if "name" in validators:
            nameMatch = self._validateName(message)
            if not nameMatch:
                return {"body": f'"{message}" não é um nome válido. Por favor, insira um nome válido.'}
        if "email" in validators:
            emailMatch = self._validateEmail(message)
            if not emailMatch:
                return {"body": f'"{message}" não é um email válido. Por favor, insira um e-mail válido.'}
        if "address" in validators:
            addressMatch = self._validateAddress(message)
            if addressMatch is False:
                return {"body": f'"{message}" não é um endereço válido. Por favor, insira um endereço válido.'}
            elif isinstance(addressMatch, str):
                return {"body": addressMatch}
        if "birthdate" in validators:
            birthdateMatch = self._validateBirthdate(message)
            if not birthdateMatch:
                return {"body": f'"{message}" não é uma data de nascimento válida. Por favor, insira uma data válida. '
                                f'Por exemplo: 30/01/1990'}

        return {"changeIntent": self.reply["nextIntent"], "parameters": {"name": message}}


def __testSignupName():
    et1 = EntryTextIntent(Replies.SIGNUP_NAME)
    firstResponse = et1.parseIncomingMessage("oii")
    print(firstResponse)
    secondResponse = et1.parseIncomingMessage("45")
    print(secondResponse)
    thirdResponse = et1.parseIncomingMessage("João")
    print(thirdResponse)


def __main():
    __testSignupName()


if __name__ == "__main__":
    __main()
