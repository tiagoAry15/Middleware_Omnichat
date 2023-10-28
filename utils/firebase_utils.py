import datetime
import uuid


def organizeSingleMessageData(messageData: dict, whatsappNumber: str, all_conversations: dict):
    uniqueId = searchUniqueIdAmongConversations(conversationData=all_conversations, userWhatsappNumber=whatsappNumber)
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    new_message = dict(messageData)
    new_message['id'] = str(uuid.uuid4())
    new_message['time'] = timestamp
    new_message.pop('from', None)
    new_message.pop('phoneNumber', None)

    if uniqueId:
        conversationData = all_conversations[uniqueId]
        conversationData["messagePot"].append(new_message)
        conversationData['lastMessage_timestamp'] = timestamp
        conversationData['unreadMessages'] += 1
        return uniqueId, conversationData
    else:
        conversationData = {
            "name": messageData['sender'],
            "status": "active",
            "phoneNumber": whatsappNumber,
            "from": messageData['from'],
            "messagePot": [new_message],
            "unreadMessages": 1,
            "lastMessage_timestamp": timestamp,
            "isBotActive": True,
        }
        return None, conversationData


def searchUniqueIdAmongConversations(conversationData: dict, userWhatsappNumber: str) -> str or None:
    if conversationData is None:
        return None
    for uniqueId, conversation in conversationData.items():
        if 'phoneNumber' in conversation and conversation['phoneNumber'] == userWhatsappNumber:
            return uniqueId
    return None


