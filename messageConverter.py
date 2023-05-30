import json
from datetime import datetime

user_message = {
    "SmsMessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
    "NumMedia": ["0"],
    "ProfileName": ["Tiago Ary"],
    "SmsSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
    "WaId": ["558599663533"],
    "SmsStatus": ["received"],
    "Body": ["Oi"],
    "To": ["whatsapp:+14155238886"],
    "NumSegments": ["1"],
    "ReferralNumMedia": ["0"],
    "MessageSid": ["SMd9c46a08ff3349af9a93dc2d40d738ff"],
    "AccountSid": ["AC034f7d97b8d5bc62dfa91b519ac43b0f"],
    "From": ["whatsapp:+558599663533"],
    "ApiVersion": ["2010-04-01"]
}

dialogflow_message = {
    "response_id": "db1b18cf-4ed9-4339-bcfd-725cf722b4b7-4c6e80df",
    "query_result": {
        "query_text": "Oi",
        "language_code": "pt-br",
        "action": "input.welcome",
        "parameters": {
            "fields": {
                "key": "time-period",
                "value": {
                    "string_value": ""
                }
            },
            "fields": {
                "key": "location",
                "value": {
                    "struct_value": {
                        "fields": {
                            "key": "zip-code",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "subadmin-area",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "street-address",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "shortcut",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "island",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "country",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "city",
                            "value": {
                                "string_value": ""
                            }
                        },
                        "fields": {
                            "key": "business-name",
                            "value": {
                                "string_value": "Oi"
                            }
                        },
                        "fields": {
                            "key": "admin-area",
                            "value": {
                                "string_value": ""
                            }
                        }
                    }
                }
            },
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
        "message": "Webhook call failed. Error: UNAVAILABLE, State: URL_UNREACHABLE, Reason: UNREACHABLE_5xx, HTTP status code: 502."
    }
}


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
