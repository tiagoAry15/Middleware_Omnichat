import json


def getTwilioBoilerPlate(body: str = "Oii"):
    return {
        "Body": body,
        "SmsMessageSid": "SM96bc23c4e756f413f24bbd4cd3386a70",
        "NumMedia": "0",
        "ProfileName": "Mateus",
        "SmsSid": "SMa14df2486670aa993e00c0a62a45a329",
        "WaId": "558599171902",
        "SmsStatus": "received",
        "To": "whatsapp:+14155238886",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SMa14df2486670aa993e00c0a62a45a329",
        "AccountSid": "AC034f7d97b8d5bc62dfa91b519ac43b0f",
        "From": "whatsapp:+558599171902",
        "ApiVersion": "2010-04-01"
    }

def getDialogflowBoilerPlate(body: str = "Oii"):
    return json.dumps({
        "responseId": "133bb879-bdbb-4151-a006-749dfb52857f-2316b108",
        "queryResult": {
            "queryText": body,
            "action": "input.welcome",
            "parameters": {},
            "allRequiredParamsPresent": True,
            "fulfillmentText": "Por favor, ligue a API",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Por favor, ligue a API"
                        ]
                    }
                }
            ],
            "outputContexts": [
                {
                    "name": "projects/pizzadobill-rpin/locations/global/agent/sessions/1b7b59ab-4d7f-9187-9c63-"
                            "2b8ad5255a0d/contexts/__system_counters__",
                    "parameters": {
                        "no-input": 0.0,
                        "no-match": 0.0
                    }
                }
            ],
            "intent": {
                "name": "projects/pizzadobill-rpin/locations/global/agent/intents/acd8e087-5400-4cf9-95f3-4c681b16b516",
                "displayName": "Welcome"
            },
            "intentDetectionConfidence": 1.0,
            "languageCode": "pt-br",
            "sentimentAnalysisResult": {
                "queryTextSentiment": {
                    "score": 0.3,
                    "magnitude": 0.3
                }
            }
        },
        "originalDetectIntentRequest": {
            "source": "DIALOGFLOW_CONSOLE",
            "payload": {}
        },
        "session": "projects/pizzadobill-rpin/locations/global/agent/sessions/1b7b59ab-4d7f-9187-9c63-2b8ad5255a0d"
    })

