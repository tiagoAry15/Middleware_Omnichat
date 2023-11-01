def get_mocked_fulfillment_request():
    intent = 'projects/pizzadobill-rpin/locations/global/agent/intents/acd8e087-5400-4cf9-95f3-4c681b16b516'
    response = 'Não foi possível se conectar ao fulfillment do dialogflow! Por favor, ligue a API'
    context = ('projects/pizzadobill-rpin/locations/global/agent/sessions/'
               'be4a8142-3002-e657-253a-159366d4b9e7/contexts/__system_counters__')
    return {'responseId': '96b43795-b334-4c35-900a-74e53e62abe2-76aba3aa',
            'queryResult': {'queryText': 'oii', 'action': 'input.welcome', 'parameters': {},
                            'allRequiredParamsPresent': True,
                            'fulfillmentText': response,
                            'fulfillmentMessages': [{'text': {'text': [response]}}],
                            'outputContexts': [{'name': context,
                                                'parameters': {'no-input': 0.0, 'no-match': 0.0}}],
                            'intent':
                                {'name': intent,
                                 'displayName': 'Welcome'}, 'intentDetectionConfidence': 1.0,
                            'languageCode': 'pt-br',
                            'sentimentAnalysisResult':
                                {'queryTextSentiment': {'score': 0.3, 'magnitude': 0.3}}},
            'originalDetectIntentRequest': {'source': 'DIALOGFLOW_CONSOLE', 'payload': {}},
            'session': 'projects/pizzadobill-rpin/locations/global/agent/sessions/be4a8142-3002-e657-253a-159366d4b9e7'}