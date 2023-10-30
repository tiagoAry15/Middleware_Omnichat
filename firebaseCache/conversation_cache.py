import datetime
from typing import List, Union

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.firebase_utils import generate_firebase_push_id


def get_dummy_conversations():
    return {
        '-NhaO-GlBOA5o7E3SyZu': {'from': 'whatsapp', 'isBotActive': True, 'lastMessage_timestamp': '25/10/2023 10:31',
                                 'messagePot': [
                                     {'body': 'Oii', 'id': '51b7e38f-75bb-452d-8463-cb01d4f34916', 'sender': 'Mateus',
                                      'time': '25/10/2023 10:31'}, {
                                         'body': 'Não foi possível se conectar ao fulfillment do dialogflow! Por '
                                                 'favor, ligue a API',
                                         'from': 'whatsapp', 'phoneNumber': '558599171902', 'sender': 'Bot',
                                         'time': '10:31'}], 'name': 'Mateus', 'phoneNumber': '558599171902',
                                 'status': 'active', 'unreadMessages': 0},
        '-Nhg7rURWmVxTJmPe8GL': {'from': 'whatsapp', 'isBotActive': True, 'lastMessage_timestamp': '2023-10-26 13:20',
                                 'messagePot': [
                                     {'body': 'oi', 'id': '68cf1641-ede7-4998-a013-12af69099dc4', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:19'}, {
                                         'body': 'Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n '
                                                 'Cardápio de pizzas:\n- Calabresa - R$17.50\n- Frango - R$18.90\n- '
                                                 'Portuguesa - R$13.99\n- Margherita - R$15.50\n- Quatro Queijos - '
                                                 'R$16.90\n- Pepperoni - R$19.99\n. \nQual pizza você vai querer?',
                                         'id': 'ae15a053-a99f-47fd-a034-afdd29f5a8a4', 'sender': 'Bot',
                                         'time': '2023-10-26 13:19'},
                                     {'body': 'oi', 'id': 'cfbd675f-4768-4353-8977-6eab09e08a6b', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:19'}, {
                                         'body': 'Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n '
                                                 'Cardápio de pizzas:\n- Calabresa - R$17.50\n- Frango - R$18.90\n- '
                                                 'Portuguesa - R$13.99\n- Margherita - R$15.50\n- Quatro Queijos - '
                                                 'R$16.90\n- Pepperoni - R$19.99\n. \nQual pizza você vai querer?',
                                         'id': 'd656dd23-3c8c-40e8-988a-941ef12d1641', 'sender': 'Bot',
                                         'time': '2023-10-26 13:19'},
                                     {'body': 'oi', 'id': '35dbbec8-d1b1-4853-aa9d-b146f6cdae96', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:20'}, {
                                         'body': 'Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n '
                                                 'Cardápio de pizzas:\n- Calabresa - R$17.50\n- Frango - R$18.90\n- '
                                                 'Portuguesa - R$13.99\n- Margherita - R$15.50\n- Quatro Queijos - '
                                                 'R$16.90\n- Pepperoni - R$19.99\n. \nQual pizza você vai querer?',
                                         'id': '01741c4e-74b5-4f51-9485-34719b1f3304', 'sender': 'Bot',
                                         'time': '2023-10-26 13:20'}], 'name': 'Tiago', 'phoneNumber': '558599663533',
                                 'status': 'active', 'unreadMessages': 0}}


def get_current_timestamp() -> str:
    return datetime.datetime.now().strftime("%d-%b-%Y at %H:%M:%S")


class ConversationCache:
    def __init__(self, conversation_connection: FirebaseConversation):
        self.firebase_connection = conversation_connection
        self.data = {}
        self._cache_miss_refresh_data()
        self.transactions = []

    def _cache_miss_refresh_data(self):
        self.data = get_dummy_conversations()

    def get_conversation_unique_id_by_whatsapp_number(self, whatsapp_number: str) -> str or None:
        for unique_id in self.data.keys():
            if self.data[unique_id]["phoneNumber"] == whatsapp_number:
                return unique_id
        return None

    def __update_messages_in_conversation(self, messages: Union[dict, List[dict]], whatsappNumber: str):
        """Helper function to update the messagePot for a given WhatsApp number."""
        unique_id = self.get_conversation_unique_id_by_whatsapp_number(whatsappNumber)
        conversation = self.data[unique_id]

        if isinstance(messages, dict):
            conversation["messagePot"].append(messages)
        elif isinstance(messages, list):
            conversation["messagePot"].extend(messages)

        self.data[unique_id] = conversation

    def append_message_to_whatsapp_number(self, messageData: dict, whatsappNumber: str):
        return self.__update_messages_in_conversation(messageData, whatsappNumber)

    def append_multiple_messages_to_whatsapp_number(self, messageData: List[dict], whatsappNumber: str):
        return self.__update_messages_in_conversation(messageData, whatsappNumber)

    def create_first_conversation(self):
        conversation_dict = {"from": "messenger", "isBotActive": True, "lastMessage_timestamp": get_current_timestamp(),
                             "messagePot": [], "name": "Bill", "phoneNumber": "558599171902", "status": "active",
                             "unreadMessages": 0}
        self.firebase_connection.createConversation(conversation_dict)

    def create_conversation(self, whatsapp_number: str, conversation_dict: dict) -> bool:
        existing_unique_id = self.get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if existing_unique_id:
            return False
        unique_id = generate_firebase_push_id()
        self.data[unique_id] = conversation_dict

    def get_conversation(self, whatsapp_number: str) -> dict or None:
        unique_id = self.get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if not unique_id:
            return None
        return self.data[unique_id]

    def update_conversation(self, whatsapp_number: str, conversation_dict: dict) -> bool:
        unique_id = self.get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if not unique_id:
            return False
        current_conversation = self.data[unique_id]
        for key, value in conversation_dict.items():
            current_conversation[key] = value
        return True


def __main():
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    cc = ConversationCache(fcm)
    whatsapp_number = "558599171902"
    # conv = cc.get_conversations(whatsapp_number)
    msgDict = {'body': 'Oii', 'from': 'whatsapp', 'phoneNumber': "558599171902", 'sender': 'Mateus',
               'time': datetime.datetime.now().strftime('%H:%M')}
    cc.append_message_to_whatsapp_number(msgDict, whatsapp_number)
    return


if __name__ == "__main__":
    __main()
