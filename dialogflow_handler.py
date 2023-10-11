import os
import uuid

import google.cloud.dialogflow_v2 as dialogflow
from twilio.twiml.messaging_response import MessagingResponse

from authentication.credentials_loader import getDialogflowCredentials
from data.speisekarte_extraction import loadSpeisekarte, createMenuString, analyzeTotalPrice
from utils.decorators.singleton_decorator import singleton


@singleton
class DialogFlowHandler:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}
        creds = getDialogflowCredentials()
        self.sessionClient = dialogflow.SessionsClient(credentials=creds)
        self.session = self.sessionClient.session_path(os.environ["SDK_PROJECT_ID"], str(uuid.uuid4()))
        self.agentName = self.session.split('/')[1]
        self.twiml = MessagingResponse()

    def getDialogFlowResponse(self, message: str, intent_name: str = None, user_number: str = None):
        session = self.session
        session_params = dialogflow.types.QueryParameters(payload={"phone-number": user_number})
        if intent_name:
            session = f"{self.session}/contexts/{intent_name}"
        textInput = dialogflow.types.TextInput(text=message, language_code='pt-BR')
        queryInput = dialogflow.types.QueryInput(text=textInput)
        requests = dialogflow.types.DetectIntentRequest(
            session=session, query_input=queryInput, query_params=session_params
        )
        return self.sessionClient.detect_intent(request=requests)

    @staticmethod
    def extractTextFromDialogflowResponse(dialogflowResponse: dialogflow.types.DetectIntentResponse):
        dialogflowResponses = dialogflowResponse.query_result.fulfillment_messages
        for response in dialogflowResponses:
            if response.text.text:
                return response.text.text[0]

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPrice(self, structuredOrder: dict):
        return analyzeTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)


def __main():
    ds = DialogFlowHandler()
    message_pool = ["Oi", "Vou querer duas pizzas de frango", "Sim", "Vou querer um guaraná", "Pix"]
    for message in message_pool:
        response = ds.getDialogFlowResponse(message=message)
        bot_answer = response.query_result.fulfillment_text
        print(bot_answer)
    return


if __name__ == "__main__":
    __main()