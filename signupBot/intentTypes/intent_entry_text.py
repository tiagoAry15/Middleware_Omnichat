import re
from datetime import datetime

from signupBot.intentTypes.base_intent import BaseIntent
from signupBot.intentTypes.replies import Replies, Types

# Constants for regular expressions
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
NAME_REGEX = r'\b[A-Za-záàâãéèêíïóôõöúçñ._%+-]+\b'
ADDRESS_REGEX = r'^(Rua|Avenida|Travessa)\s[^\d]*\d+$'
DATE_REGEX = r'\b\d{2}\/\d{2}\/\d{4}\b'
CPF_REGEX = r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$'

# Constants for field names
NAME = "name"
EMAIL = "email"
ADDRESS = "address"
BIRTHDATE = "birthdate"
CPF = "cpf"


class EntryTextIntent(BaseIntent):
    """Full Name, Email, Delivery Address, Birthdate, Phone Number, CEP, etc."""

    def __init__(self, coreReply: Replies):
        super().__init__(coreReply)
        self.validators = {
            NAME: self._validateName,
            EMAIL: self._validateEmail,
            ADDRESS: self._validateAddress,
            BIRTHDATE: self._validateBirthdate,
            CPF: self._validateCPF
        }

    def getIntentType(self) -> str:
        return Types.ENTRY_TEXT

    def _produceFirstSentence(self) -> str:
        return self.reply["main"]

    @staticmethod
    def _validateEmail(email: str) -> bool or dict:
        pattern = EMAIL_REGEX
        match = re.match(pattern, email)
        failMessage = "Email inválido. Por favor, insira um email válido."
        return {"output": "success"} if match else {"output": "failure", "outputDetails": failMessage}

    @staticmethod
    def _validateName(name: str) -> bool or dict:
        pattern = NAME_REGEX
        match = re.match(pattern, name)
        failMessage = "Nome inválido. Por favor, insira um nome válido."
        return {"output": "success"} if match else {"output": "failure", "outputDetails": failMessage}

    @staticmethod
    def _validateAddress(address: str) -> bool or dict:
        formattedAddress = ' '.join(word.title() if word.isalpha() else word for word in address.split())
        pattern = ADDRESS_REGEX
        match = re.match(pattern, formattedAddress)

        if not match:
            if not re.match(r'^(Rua|Avenida|Travessa)', formattedAddress):
                addressType = formattedAddress.split(' ')[0]
                failMessage = f"{addressType} é um tipo de endereço inválido. Por favor, use um tipo válido " \
                              f"por exemplo Rua, Avenida, Travessa, etc)"
                return {"output": "failure", "outputDetails": failMessage}
            elif not re.search(r'\d', formattedAddress):
                failMessage = "Endereço inválido. Está faltando o número da casa."
                return {"output": "failure", "outputDetails": failMessage}
            else:
                return {"output": "failure",
                        "outputDetails": "Endereço inválido. Por favor, insira um endereço válido."}
        return {"output": "success"}

    @staticmethod
    def _validateBirthdate(birthdate: str) -> bool or dict:
        if not re.match(DATE_REGEX, birthdate):
            return {"output": "failure", "outputDetails": f"{birthdate} é uma data inválida. "
                                                          f"Por favor, insira uma data de nascimento válida."}
        try:
            datetime.strptime(birthdate, '%d/%m/%Y')
            return {"output": "success", "outputDetails": "ACTION_ASSEMBLY_SIGNUP"}
        except ValueError:
            return {"output": "failure", "outputDetails": f"{birthdate} é uma data inválida. "
                                                          f"Por favor, insira uma data de nascimento válida."}

    @staticmethod
    def _validateCPF(cpf: str) -> bool or dict:
        cpf = cpf.replace(".", "").replace("-", "")  # Remove dots and hyphen from CPF
        return (
            {"output": "success", "outputDetails": "ACTION_ASSEMBLY_SIGNUP"}
            if re.match(CPF_REGEX, cpf)
            else {
                "output": "failure",
                "outputDetails": f"{cpf} é um CPF inválido. Por favor, insira um CPF válido.",
            }
        )

    def parseIncomingMessage(self, message: str) -> dict:
        if not self.alreadyWelcomed:
            return self.sendFirstMessage()

        validators = self.reply["validators"] if self.reply["validators"] is not None else []
        for validator in validators:
            return self.processValidation(validator, message)

    def processValidation(self, validator, message):
        validateFunction = self.validators[validator]
        matchResult = validateFunction(message)
        output = matchResult["output"] if isinstance(matchResult, dict) else None
        outputDetails = matchResult.get("outputDetails", None)
        if outputDetails is not None and "ACTION" in outputDetails:
            rawAction = outputDetails.split("_")[1:]
            action = '_'.join(rawAction)
        else:
            action = None
        return (
            {
                "changeIntent": self.reply["nextIntent"],
                "parameters": {validator: message},
                "action": action,
            }
            if output == "success"
            else {"body": outputDetails}
        )


def __testSignupName():
    et1 = EntryTextIntent(Replies.SIGNUP_CPF)
    firstResponse = et1.parseIncomingMessage("oii")
    print(firstResponse)
    secondResponse = et1.parseIncomingMessage("03874832333")
    print(secondResponse)


def __main():
    __testSignupName()


if __name__ == "__main__":
    __main()
