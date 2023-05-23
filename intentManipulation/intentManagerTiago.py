class IntentManager:

    def __init__(self):
        self.intent_dict = {
            'WELCOME': (self.handle_welcome_intent, 1),
        'despedida': (self.handle_goodbye_intent, 1),
        'informacao': (self.handle_information_intent, 1)
}

    def process_intent(self, gpt_response):
        if gpt_response.intent == 'WELCOME':
            return self.handle_welcome_intent(gpt_response)
        else:
            return self.handle_unknown_intent()
    def handle_welcome_intent(self, response):
        image_url = "https://shorturl.at/lEFT0"
        return {'content': response.body, 'media': image_url}
    def handle_goodbye_intent(self):
        print("Até logo! Volte sempre.")

    def handle_information_intent(self):
        print("Que tipo de informação você está procurando?")

    def handle_unknown_intent(self):
        return {'content': 'Não entendi', 'media': ''}


