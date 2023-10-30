from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation, getDummyConversationDicts


def __createDummyConversations():
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    dictPot = []
    dictParameters = ("John", "+558599171902", "whatsapp",
                      "Maria", "+558599171903", "instagram",
                      "Anthony", "+558599171904", "messenger")
    for username, phoneNumber, _from in zip(dictParameters[::3], dictParameters[1::3], dictParameters[2::3]):
        dicts = getDummyConversationDicts(username=username, phoneNumber=phoneNumber, _from=_from)
        dictPot.append(dicts)
    for _dict in dictPot:
        for conversation in _dict["dummyPot"]:
            fcm.createConversation(conversation)


def __main():
    __createDummyConversations()


if __name__ == "__main__":
    __main()
