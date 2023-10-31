import datetime
import random
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
                                         'body': 'Olá meu querido, tudo bem?',
                                         'from': 'whatsapp', 'phoneNumber': '558599171902', 'sender': 'Bot',
                                         'time': '10:31'}], 'name': 'Mateus', 'phoneNumber': '558599171902',
                                 'status': 'active', 'unreadMessages': 0},
        '-Nhg7rURWmVxTJmPe8GL': {'from': 'whatsapp', 'isBotActive': True, 'lastMessage_timestamp': '2023-10-26 13:20',
                                 'messagePot': [
                                     {'body': 'Oii', 'id': '68cf1641-ede7-4998-a013-12af69099dc4', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:19'},
                                     {'body': 'Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n '
                                              'Cardápio de pizzas:\n- Calabresa - R$17.50\n- Frango - R$18.90\n- '
                                              'Portuguesa - R$13.99\n- Margherita - R$15.50\n- Quatro Queijos - '
                                              'R$16.90\n- Pepperoni - R$19.99\n. \nQual pizza você vai querer?',
                                      'id': 'ae15a053-a99f-47fd-a034-afdd29f5a8a4', 'sender': 'Bot',
                                      'time': '2023-10-26 13:19'},

                                     {'body': 'Vou querer uma pizza meio frango meio calabresa',
                                      'id': 'cfbd675f-4768-4353-8977-6eab09e08a6b', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:19'}, {
                                         'body': 'Certo, uma pizza meio frango meio calabresa saindo então!'
                                                 ' Vai querer bebida?',
                                         'id': 'd656dd23-3c8c-40e8-988a-941ef12d1641', 'sender': 'Bot',
                                         'time': '2023-10-26 13:19'},

                                     {'body': 'Vou querer um suco de laranja',
                                      'id': '35dbbec8-d1b1-4853-aa9d-b146f6cdae96', 'sender': 'Tiago',
                                      'time': '2023-10-26 13:20'}, {
                                         'body': 'Maravilha então!', 'sender': 'Bot',
                                         'time': '2023-10-26 13:20'}], 'name': 'Tiago', 'phoneNumber': '558599663533',
                                 'status': 'active', 'unreadMessages': 0}}


def get_firebase_inconsistent_data() -> dict:
    """
    Simulate pulling modified data from Firebase by introducing random modifications.
    Represents changes made by other backend replicas.
    """
    data = get_dummy_conversations()
    for unique_id, conversation in data.items():
        # Randomly modify the last message for simulation
        if random.choice([True, False]):
            last_message = conversation["messagePot"][-1]
            new_message_body = last_message["body"] + " (Modified by Replica)"
            last_message["body"] = new_message_body
            conversation["messagePot"][-1] = last_message

            # Update the timestamp of last message
            timestamp = conversation["lastMessage_timestamp"]
            timestamp_datetime = convert_to_datetime(timestamp)
            new_timestamp = timestamp_datetime + datetime.timedelta(minutes=random.randint(1, 60))
            conversation["lastMessage_timestamp"] = new_timestamp.strftime("%d/%m/%Y %H:%M")

    return data


def get_current_timestamp() -> str:
    return datetime.datetime.now().strftime("%d-%b-%Y at %H:%M:%S")


def convert_to_datetime(timestamp: str) -> datetime.datetime:
    """
    Convert the string timestamp to a datetime object for comparison.
    """
    try:
        # If timestamp is in "dd/mm/yyyy HH:MM" format
        return datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
    except ValueError:
        try:
            # If timestamp is in "dd-bbb-yyyy at HH:MM:SS" format
            return datetime.datetime.strptime(timestamp, "%d-%b-%Y at %H:%M:%S")
        except Exception as e:
            raise ValueError("Timestamp format not recognized")


def get_inconsistent_conversations() -> dict:
    """
    Simulate pulling inconsistent data from Firebase by introducing random inconsistencies.
    """
    data = get_dummy_conversations()
    for unique_id, conversation in data.items():
        # Randomly change the timestamp for simulation
        if random.choice([True, False]):
            timestamp = conversation["lastMessage_timestamp"]
            timestamp_datetime = convert_to_datetime(timestamp)
            new_timestamp = timestamp_datetime + datetime.timedelta(minutes=random.randint(1, 60))
            conversation["lastMessage_timestamp"] = new_timestamp.strftime("%d/%m/%Y %H:%M")
    return data


class ConversationCache:
    def __init__(self, conversation_connection: FirebaseConversation):
        self.firebase_connection = conversation_connection
        self.data = {}
        self._cache_miss_refresh_data()
        self.transactions = []

    def _cache_miss_refresh_data(self):
        self.data = get_dummy_conversations()

    def __get_conversation_unique_id_by_whatsapp_number(self, whatsapp_number: str) -> str or None:
        for unique_id in self.data.keys():
            if self.data[unique_id]["phoneNumber"] == whatsapp_number:
                return unique_id
        return None

    def __update_messages_in_conversation(self, messages: Union[dict, List[dict]], whatsappNumber: str):
        """Helper function to update the messagePot for a given WhatsApp number."""
        unique_id = self.__get_conversation_unique_id_by_whatsapp_number(whatsappNumber)
        conversation = self.data[unique_id]

        if isinstance(messages, dict):
            conversation["messagePot"].append(messages)
        elif isinstance(messages, list):
            conversation["messagePot"].extend(messages)

        self.data[unique_id] = conversation

    def __create_first_conversation(self):
        conversation_dict = {"from": "messenger", "isBotActive": True, "lastMessage_timestamp": get_current_timestamp(),
                             "messagePot": [], "name": "Bill", "phoneNumber": "558599171902", "status": "active",
                             "unreadMessages": 0}
        self.firebase_connection.createConversation(conversation_dict)

    def append_message_to_whatsapp_number(self, messageData: dict, whatsappNumber: str):
        return self.__update_messages_in_conversation(messageData, whatsappNumber)

    def append_multiple_messages_to_whatsapp_number(self, messageData: List[dict], whatsappNumber: str):
        return self.__update_messages_in_conversation(messageData, whatsappNumber)

    def create_conversation(self, whatsapp_number: str, conversation_dict: dict) -> bool:
        existing_unique_id = self.__get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if existing_unique_id:
            return False
        unique_id = generate_firebase_push_id()
        self.data[unique_id] = conversation_dict

    def get_conversation(self, whatsapp_number: str) -> dict or None:
        unique_id = self.__get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if not unique_id:
            return None
        return self.data[unique_id]

    def update_conversation(self, whatsapp_number: str, conversation_dict: dict) -> bool:
        unique_id = self.__get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if not unique_id:
            return False
        current_conversation = self.data[unique_id]
        for key, value in conversation_dict.items():
            current_conversation[key] = value
        return True

    def delete_conversation(self, whatsapp_number: str) -> bool:
        unique_id = self.__get_conversation_unique_id_by_whatsapp_number(whatsapp_number)
        if not unique_id:
            return False
        self.data.pop(unique_id)
        return True


def __main():
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    cc = ConversationCache(fcm)
    whatsapp_number = "558599171902"
    # conv = cc.get_conversations(whatsapp_number)
    # msgDict = {'body': 'Oii', 'from': 'whatsapp', 'phoneNumber': "558599171902", 'sender': 'Mateus',
    #            'time': datetime.datetime.now().strftime('%H:%M')}
    # cc.append_message_to_whatsapp_number(msgDict, whatsapp_number)
    inconsistent_data = get_inconsistent_conversations()
    return


if __name__ == "__main__":
    __main()
