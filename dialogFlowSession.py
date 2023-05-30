import os
import google.cloud.dialogflow_v2 as dialogflow
from twilio.twiml.messaging_response import MessagingResponse

from data.speisekarteExtraction import loadSpeisekarte, createMenuString, analyzeTotalPrice


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def update_connection_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.updateConnection()
        return func(self, *args, **kwargs)
    return wrapper


@singleton
class DialogFlowSession:
    def __init__(self):
        self.speisekarte = loadSpeisekarte()
        self.params = {"pizzas": [], "drinks": []}
        dialogflowJsonFilePath = os.path.join(os.getcwd(), 'dialogflow.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dialogflowJsonFilePath
        self.sessionClient = dialogflow.SessionsClient()
        self.session = self.sessionClient.session_path(os.environ["DIALOGFLOW_PROJECT_ID"], "abc")
        self.agentName = self.session.split('/')[1]
        self.twiml = MessagingResponse()

    def getDialogFlowResponse(self, message: str, intent_name: str = None):
        session = self.session
        if intent_name:
            session = f"{self.session}/contexts/{intent_name}"
        textInput = dialogflow.types.TextInput(text=message, language_code='pt-BR')
        queryInput = dialogflow.types.QueryInput(text=textInput)
        requests = dialogflow.types.DetectIntentRequest(session=session, query_input=queryInput)
        # return self.sessionClient.detect_intent(request=requests)
        return self.sessionClient.detect_intent(
            session=self.session, query_input=queryInput
        )

    @staticmethod
    def extractTextFromDialogflowResponse(dialogflowResponse: dialogflow.types.DetectIntentResponse):
        dialogflowResponses = dialogflowResponse.query_result.fulfillment_messages
        for response in dialogflowResponses:
            if response.text.text:
                return response.text.text[0]

    def sendTwilioRawMessage(self, desiredMessage: str, image_url: str = None):
        message = self.twiml.message(desiredMessage)
        if image_url:
            message.media(image_url)
        return self.twiml

    def getDrinksString(self):
        return createMenuString(menu=self.speisekarte["Bebidas"], category="bebidas")

    def getPizzasString(self):
        return createMenuString(menu=self.speisekarte["Pizzas"], category="pizzas")

    def analyzeTotalPrice(self, structuredOrder: dict):
        return analyzeTotalPrice(structuredOrder=structuredOrder, menu=self.speisekarte)
