import uuid
from typing import List

from dialogFlowSession import singleton, update_connection_decorator
from firebaseFolder.firebaseConnection import FirebaseConnection
from firebaseFolder.firebaseCoreWrapper import FirebaseWrapper


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
            if "phoneNumber" in conversationData and conversationData["phoneNumber"] == whatsappNumber:
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
        return self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)

    def retrieveAllMessagesByWhatsappNumber(self, whatsappNumber: str) -> List[dict] or None:
        uniqueId = self.getUniqueIdByWhatsappNumber(whatsappNumber)
        if not uniqueId:
            return None
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if "messagePot" not in conversationData:
            return None
        return conversationData["messagePot"]

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
        if 'unreadMessages' not in conversationData:
            conversationData["unreadMessages"] = []
        if 'unreadMessages' not in messageData:
            conversationData['lastMessage'] = messageData
            conversationData["unreadMessages"].append(messageData)
        else:
            conversationData["unreadMessages"] = messageData["unreadMessages"]

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

def __createDummyConversations():
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    dummyMessagePot = [{"message": "Olá, tudo bem?"},
                       {"message": "Sim, estou bem e você?"},
                       {"message": "Estou bem também, obrigado por perguntar!"}]
    dummyPot = [{"messagePot": dummyMessagePot, "userNumber": "whatsapp:+5585994875482"},
                {"messagePot": [], "userNumber": "whatsapp:+5585935478125"},
                {"messagePot": [], "userNumber": "whatsapp:+5585948978154"}]
    for message in dummyPot:
        fcm.createConversation(message)


def __main():
    # __createDummyConversations()
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    fcm.deleteAllConversations()
    # fcm.appendMessageToWhatsappNumber({"message": "Olá, tudo bem?"}, "whatsapp:+5585994875482")
    # fc = FirebaseConnection()
    # fm = FirebaseConversation(fc)
    # print(fm.existingConversation({"conversationId": "1"}))


if __name__ == "__main__":
    __main()
