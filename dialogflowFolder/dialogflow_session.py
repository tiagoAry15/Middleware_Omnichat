import os

from authentication.credentials_loader import getDialogflowCredentials
import google.cloud.dialogflow_v2 as dialogflow


class DialogflowSession:
    def __init__(self):
        creds = getDialogflowCredentials()
        self.sessionClient = dialogflow.SessionsClient(credentials=creds)
        self.session = None
        self.agentName = None

    def initialize_session(self, user_id: str):
        self.session = self.sessionClient.session_path(os.environ["SDK_PROJECT_ID"], user_id)
        self.agentName = self.session.split('/')[1]

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


def __main():
    ds = DialogflowSession()
    response_dict = {}
    message_pool = ["Oi", "Vou querer duas pizzas de frango", "Sim", "Vou querer um guaraná", "Pix"]
    for message in message_pool:
        response = ds.getDialogFlowResponse(message=message)
        bot_answer = response.query_result.fulfillment_text
        response_dict[message] = bot_answer
    return


if __name__ == "__main__":
    __main()
