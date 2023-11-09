mock_twilio_sandbox = {
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

mock_order_1 = {
    "address": "Rua da Justiça 9584",
    "communication": "Janderson@bol.com.br",
    "customerName": "Janderson",
    "observation": "Tirar cebola",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Portuguesa"],
            "size": "Large",
            "quantity": 1,
            "price": 15.00
        },
        {
            "type": "drink",
            "flavors": ["Coca-Cola"],
            "size": "2L",
            "quantity": 1,
            "price": 2.50
        },
        {
            "type": "pizza",
            "flavors": ["Margarita", "Frango com Catupiry"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        }
    ],
    "platform": "Instagram",
    "status": "Em preparação",
    "timestamp": "30_Oct_2023_10_54_31_582"
},
mock_order_2 = {
    "address": "Rua Marcos Macedo 700",
    "communication": "558599663533",
    "customerName": "Mateus",
    "observation": "None",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Portuguesa"],
            "size": "Large",
            "quantity": 1,
            "price": 15.00
        },
        {
            "type": "drink",
            "flavors": ["Guaraná"],
            "size": "2L",
            "quantity": 1,
            "price": 2.50
        },
        {
            "type": "pizza",
            "flavors": ["Margarita", "Frango com Catupiry"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        }
    ],
    "platform": "WhatsApp",
    "status": "Em preparação",

}
webhookForIntent = {"responseId": "e41144bf-e292-4a68-acbd-0f600cdfb934-1838fa0d",
                    "queryResult": {"queryText": "uma pizza de calabresa",
                                    "parameters": {"flavor": ["calabresa"], "quantity": [], "Fraction": []},
                                    "fulfillmentText": "What is the quantity?",
                                    "fulfillmentMessages": [{"text": {"text": ["What is the quantity?"]}}],
                                    "outputContexts": [{
                                                           "name": "projects/catupirybase/locations/global/agent/sessions/f003b134-261b-fb71-f629-6eb8788160cb/contexts/155c3759-259a-433c-a909-3a695f1441a6_id_dialog_context",
                                                           "lifespanCount": 2,
                                                           "parameters": {"flavor": ["calabresa"],
                                                                          "flavor.original": ["calabresa"],
                                                                          "quantity": [],
                                                                          "quantity.original": [],
                                                                          "Fraction": [],
                                                                          "Fraction.original": []}},
                                                       {
                                                           "name": "projects/catupirybase/locations/global/agent/sessions/f003b134-261b-fb71-f629-6eb8788160cb/contexts/order_pizza_dialog_context",
                                                           "lifespanCount": 2,
                                                           "parameters": {"flavor": ["calabresa"],
                                                                          "flavor.original": ["calabresa"],
                                                                          "quantity": [],
                                                                          "quantity.original": [],
                                                                          "Fraction": [],
                                                                          "Fraction.original": []}},
                                                       {
                                                           "name": "projects/catupirybase/locations/global/agent/sessions/f003b134-261b-fb71-f629-6eb8788160cb/contexts/order_pizza_dialog_params_quantity",
                                                           "lifespanCount": 1,
                                                           "parameters": {"flavor": ["calabresa"],
                                                                          "flavor.original": ["calabresa"],
                                                                          "quantity": [],
                                                                          "quantity.original": [],
                                                                          "Fraction": [],
                                                                          "Fraction.original": []}},
                                                       {
                                                           "name": "projects/catupirybase/locations/global/agent/sessions/f003b134-261b-fb71-f629-6eb8788160cb/contexts/_system_counters_",
                                                           "lifespanCount": 1,
                                                           "parameters": {"no-input": 0.0,
                                                                          "no-match": 0.0,
                                                                          "flavor": ["calabresa"],
                                                                          "flavor.original": ["calabresa"],
                                                                          "quantity": [],
                                                                          "quantity.original": [],
                                                                          "Fraction": [],
                                                                          "Fraction.original": []}}],
                                    "intent": {
                                        "name": "projects/catupirybase/locations/global/agent/intents/155c3759-259a-433c-a909-3a695f1441a6",
                                        "displayName": "Order.pizza"},
                                    "intentDetectionConfidence": 0.74105006,
                                    "languageCode": "pt-br",
                                    "sentimentAnalysisResult": {"queryTextSentiment": {"score": 0.1,
                                                                                       "magnitude": 0.1}}},
                    "originalDetectIntentRequest": {"source": "DIALOGFLOW_CONSOLE",
                                                    "payload": {}},
                    "session": "projects/catupirybase/locations/global/agent/sessions/f003b134-261b-fb71-f629-6eb8788160cb"}
