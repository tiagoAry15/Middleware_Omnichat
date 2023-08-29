import json
from datetime import datetime


class MessageConverter:
    @staticmethod
    def convert_user_message(userMessage):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        social_network, telephone = userMessage['From'][0].split(":")
        message_dict = {
            'sender': userMessage['ProfileName'][0],
            'from': social_network,
            'telephone': telephone,
            'body': userMessage['Body'][0],
            "time": current_time

        }
        return message_dict

    @staticmethod
    def convert_dialogflow_message(dialogflowMessage, userNumber):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        message_dict = {
            'sender': "ChatBot",
            'telephone': userNumber,
            'body': dialogflowMessage['query_result']['fulfillment_text'],
            "time": current_time
        }
        return message_dict


