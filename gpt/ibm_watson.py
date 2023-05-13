import os

from dotenv import load_dotenv
from ibm_watson import AssistantV2


class WatsonAssistant:
    def __init__(self):
        apiKey = os.environ["ASSISTANT_IAM_APIKEY"]
        url = os.environ["ASSISTANT_URL"]
        self.assistant = AssistantV2(
            version='2021-06-14',
            iam_apikey=apiKey,
        )
        self.assistant.set_service_url(
            'https://api.us-south.assistant.watson.cloud.ibm.com/instances/9b9c7a5c-4a7a-4a5a-9c3f-6b7b2f1f3f5b')


def __main():
    load_dotenv()
    w = WatsonAssistant()
