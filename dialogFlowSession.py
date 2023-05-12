import os
import google.cloud.dialogflow_v2 as dialogflow
from twilio.twiml.messaging_response import MessagingResponse


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DialogFlowSession:
    def __init__(self):
        dialogflowJsonFilePath = os.path.join(os.getcwd(), 'dialogflow.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dialogflowJsonFilePath
        self.sessionClient = dialogflow.SessionsClient()
        self.session = self.sessionClient.session_path(os.environ["DIALOGFLOW_PROJECT_ID"], "abc")
        self.agentName = self.session.split('/')[1]
        self.twiml = MessagingResponse()

    def getDialogFlowResponse(self, message: str):
        textInput = dialogflow.types.TextInput(text=message, language_code='pt-BR')
        queryInput = dialogflow.types.QueryInput(text=textInput)
        return self.sessionClient.detect_intent(
            session=self.session, query_input=queryInput
        )

    def sendTwilioMessage(self, dialogflowResponse: dialogflow.types.DetectIntentResponse):
        detectedIntent = dialogflowResponse.query_result.intent.display_name
        dialogflowResponses = dialogflowResponse.query_result.fulfillment_messages
        for response in dialogflowResponses:
            if response.text.text:
                text = response.text.text[0]
                self.twiml.message(text)
            if response.payload:
                fields = response.payload.fields
                message = self.twiml.message()
                if fields.get('mediaUrl'):
                    media_url = fields.get('mediaUrl').string_value
                    message.media(media_url)
                if fields.get('text'):
                    text = fields.get('text').string_value
                    message.body(text)
