import json
from datetime import datetime




class MessageConverter:
    @staticmethod
    def convert_user_message(userMessage):
        # user_message_dict = json.loads(user_message)
        social_network, telephone = userMessage['From'][0].split(":")
        message_dict = {
            'sender': userMessage['ProfileName'][0],
            'from': social_network,
            'telephone': telephone,
            'body': userMessage['Body'][0],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")

        }
        return message_dict

    @staticmethod
    def convert_dialogflow_message(dialogflowMessage, userNumber):
        message_dict = {
            'sender': "ChatBot",
            'telephone': userNumber,
            'body': dialogflowMessage['query_result']['fulfillment_text'],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        return message_dict


def __main():
    print(MessageConverter.convert_user_message(json.dumps(user_message)))

    print(MessageConverter.convert_dialogflow_message(json.dumps(dialogflow_message)))


if __name__ == '__main__':
    __main()
