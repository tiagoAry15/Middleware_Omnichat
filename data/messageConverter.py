import json
from datetime import datetime


def get_user_message_example():
    return {
        "SmsMessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "NumMedia": ["0"],
        "ProfileName": ["Tiago"],
        "SmsSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "WaId": ["558588567446"],
        "SmsStatus": ["received"],
        "Body": ["oi"],
        "To": ["whatsapp:+14155238886"],
        "NumSegments": ["1"],
        "ReferralNumMedia": ["0"],
        "MessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
        "AccountSid": ["AC034f7d97b8d5bc62dfa91b519ac43b0f"],
        "From": ["whatsapp:+558599663533"],
        "ApiVersion": ["2010-04-01"]
    }


def get_dialogflow_message_example():
    return {
        "response_id": "db1b18cf-4ed9-4339-bcfd-725cf722b4b7-4c6e80df",
        "query_result": {
            "query_text": "Oi",
            "language_code": "pt-br",
            "action": "input.welcome",
            "parameters": {
                "fields": {
                    "key": "date-time",
                    "value": {
                        "string_value": ""
                    }
                }
            },
            "all_required_params_present": "True",
            "fulfillment_text": "Por favor, ligue a API",
            "fulfillment_messages": {
                "text": {
                    "text": "Por favor, ligue a API"
                }
            },
            "intent": {
                "name": "projects/pizzadobill-rpin/agent/intents/acd8e087-5400-4cf9-95f3-4c681b16b516",
                "display_name": "Welcome"
            },
            "intent_detection_confidence": 1,
            "diagnostic_info": {
                "fields": {
                    "key": "webhook_latency_ms",
                    "value": {
                        "number_value": 2889
                    }
                }
            }
        },
        "webhook_status": {
            "code": 14,
            "message": "Webhook call failed. Error: UNAVAILABLE, State: URL_UNREACHABLE, Reason: UNREACHABLE_5xx,"
                       " HTTP status code: 502."
        }
    }


class MessageConverter:
    def __init__(self):
        self._from = ""
        self.phoneNumber = ""
        self.sender = ""

    def setMessageCoreDetails(self, sender: str, _from: str, phoneNumber: str):
        self.sender = sender
        self._from = _from
        self.phoneNumber = phoneNumber

    def dynamicConversion(self, message: str):
        return {
            'sender': self.sender,
            'from': self._from,
            'phoneNumber': self.phoneNumber,
            'body': message,
            "time": datetime.now().strftime("%H:%M"),
        }

    @staticmethod
    def convert_user_message(userMessage):

        social_network, userNumber = userMessage['From'][0].split(":")
        sender = userMessage['ProfileName'][0] if social_network == "whatsapp" else userNumber
        receivedMessage = userMessage['Body'][0]

        return {
            'sender': sender,
            'from': social_network,
            'phoneNumber': userNumber,
            'body': receivedMessage,
            "time": datetime.now().strftime("%H:%M"),
        }

    @staticmethod
    def convert_dialogflow_message(dialogflowMessage, userNumber):
        return {
            'sender': "ChatBot",
            'phoneNumber': userNumber,
            'body': dialogflowMessage,
            "time": datetime.now().strftime("%H:%M"),
        }


def __main():
    print(MessageConverter.convert_user_message(json.dumps(get_user_message_example())))
    print(MessageConverter.convert_dialogflow_message(json.dumps(get_dialogflow_message_example())))


if __name__ == '__main__':
    __main()
