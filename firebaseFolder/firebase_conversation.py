import datetime
import random
import uuid
from typing import List

from dialogflow_session import singleton, update_connection_decorator
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_coreWrapper import FirebaseWrapper


@singleton
class FirebaseConversation(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("conversations")

    def getAllConversations(self):
        return self.firebaseConnection.readData()

    def getUniqueIdByWhatsappNumber(self, whatsappNumber: str) -> str or None:
        # sourcery skip: use-next
        allConversations = self.getAllConversations()
        if allConversations is None:
            return None
        for uniqueId, conversationData in allConversations.items():
            phoneNumber = conversationData.get("phoneNumber", None)
            if phoneNumber == whatsappNumber:
                return uniqueId
        return None

    def appendMessageToWhatsappNumber(self, messageData: dict, whatsappNumber: str):
        uniqueId = self.getUniqueIdByWhatsappNumber(whatsappNumber)
        if not uniqueId:
            return False
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if "messagePot" not in conversationData:
            conversationData["messagePot"] = []
        messageData["id"] = str(uuid.uuid4())
        conversationData["messagePot"].append(messageData)
        self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)
        return messageData

    def retrieveAllMessagesByWhatsappNumber(self, whatsappNumber: str) -> List[dict] or None:
        uniqueId = self.getUniqueIdByWhatsappNumber(whatsappNumber)
        if not uniqueId:
            return None
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if "messagePot" not in conversationData:
            return None
        return conversationData["messagePot"]

    def createFirstDummyConversationByWhatsappNumber(self, msgDict: dict):
        whatsappNumber = msgDict.get("phoneNumber", None)
        body = msgDict.get("body", None)
        name = msgDict.get("name", None)
        platform = msgDict.get("from", None)
        currentTime = datetime.datetime.now().strftime("%H:%M")
        conversationData = {"from": platform, "whatsappNumber": whatsappNumber, "id": 0, "name": name,
                            "status": "active", "unreadMessages": 1,
                            "msgPot": [{"body": body, "id": str(uuid.uuid4()), "phoneNumber": "+5585999171902",
                                        "sender": "User", "time": currentTime}]}
        self.firebaseConnection.writeData(data=conversationData)
        return "Dummy conversation created successfully."

    def existingConversation(self, inputConversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(inputConversationData["phoneNumber"])
        return uniqueId is not None

    def createConversation(self, conversationData: dict) -> bool:
        existingConversation = self.existingConversation(conversationData)
        return (
            False if existingConversation
            else self.firebaseConnection.writeData(data=conversationData)
        )

    def updateConversation(self, conversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(conversationData["phoneNumber"])
        return (
            self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)
            if uniqueId is not None
            else False
        )

    def updateConversationAddingUnreadMessages(self, messageData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(messageData["phoneNumber"])
        if not uniqueId:
            return None
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if 'unreadMessages' not in messageData:
            conversationData["unreadMessages"] = conversationData["unreadMessages"] + 1
        else:
            conversationData["unreadMessages"] = 0
        self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)
        return conversationData

    def deleteConversation(self, conversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(conversationData["phoneNumber"])
        return (
            self.firebaseConnection.deleteData(path=uniqueId)
            if uniqueId is not None
            else False
        )

    def deleteAllConversations(self):
        return self.firebaseConnection.deleteAllData()


def getDummyConversationDicts(username: str = "John", phoneNumber: str = "+558599171902", _from: str = "whatsapp"):
    dummyBodyMessages = ["Olá, tudo bem?", "Sim estou bem, e você?", "Estou bem também, obrigado por perguntar!"]
    dummyMessagePot = []
    for index, body in enumerate(dummyBodyMessages):
        currentFormattedTimestamp = datetime.datetime.now().strftime("%H:%M")
        sender = "ChatBot" if index % 2 == 1 else username
        message = {"body": body, "id": random.randint(0, 10000000000), "phoneNumber": phoneNumber,
                   "sender": sender, "timestamp": currentFormattedTimestamp}
        dummyMessagePot.append(message)

    dummyPot = [{"from": _from, "id": 3, "name": username, "phoneNumber": phoneNumber, "status": "active",
                 "messagePot": dummyMessagePot, "lastMessage": dummyMessagePot[-1], "unreadMessages": 1}]
    return {"dummyMessagePot": dummyMessagePot, "dummyPot": dummyPot}


def __createDummyConversations():
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    dictPot = []
    dictParameters = ("John", "+558599171902", "whatsapp",
                      "Maria", "+558599171903", "instagram",
                      "Anthony", "+558599171904", "facebook")
    for username, phoneNumber, _from in zip(dictParameters[::3], dictParameters[1::3], dictParameters[2::3]):
        dicts = getDummyConversationDicts(username=username, phoneNumber=phoneNumber, _from=_from)
        dictPot.append(dicts)
    for _dict in dictPot:
        for conversation in _dict["dummyPot"]:
            fcm.createConversation(conversation)


def checkNewUser(whatsappNumber: str, numberPot: List[str],
                 conversationInstance: FirebaseConversation, msgDict: dict) -> bool:
    if whatsappNumber in numberPot:
        return False
    numberPot.append(whatsappNumber)
    conversationInstance.createFirstDummyConversationByWhatsappNumber(msgDict)
    return True


def __main():
    # __createDummyConversations()
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    randomUniqueId = str(uuid.uuid4())
    currentTime = datetime.datetime.now().strftime("%H:%M")
    msgDict = {"body": "Olá, tudo bem?", "id": str(uuid.uuid4()), "phoneNumber": "+5585999171902",
               "sender": "Mateus", "time": datetime.datetime.now().strftime("%H:%M")}
    fcm.appendMessageToWhatsappNumber(msgDict, "+5585999171902")
    # msgDict = {"phoneNumber": "+5585994875485", "body": "Olá, tudo bem?", "name": "Maria", "from": "facebook"}
    # fcm.createFirstDummyConversationByWhatsappNumber(msgDict)
    # createDummyConversations()
    # fcm.deleteAllConversations()
    # fcm.appendMessageToWhatsappNumber({"message": "Olá, tudo bem?"}, "whatsapp:+5585994875482")
    # fc = FirebaseConnection()
    # fm = FirebaseConversation(fc)
    # print(fm.existingConversation({"conversationId": "1"}))


if __name__ == "__main__":
    __main()
