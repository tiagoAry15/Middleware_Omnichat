import os
import dotenv
from google.oauth2 import service_account
from google.cloud import dialogflow_v2
from google.protobuf import field_mask_pb2

from utils.decorators.time_decorator import timingDecorator


def getDialogflowCredentials():
    credentials_info = {
        "type": os.environ["DIALOGFLOW_TYPE"],
        "project_id": os.environ["DIALOGFLOW_PROJECT_ID"],
        "private_key_id": os.environ["DIALOGFLOW_PRIVATE_KEY_ID"],
        "private_key": os.environ["DIALOGFLOW_PRIVATE_KEY"].replace("\\n", "\n").strip(),
        "client_email": os.environ["DIALOGFLOW_CLIENT_EMAIL"],
        "client_id": os.environ["DIALOGFLOW_CLIENT_ID"],
        "auth_uri": os.environ["DIALOGFLOW_AUTH_URI"],
        "token_uri": os.environ["DIALOGFLOW_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["DIALOGFLOW_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["DIALOGFLOW_CLIENT_X509_CERT_URL"]
    }
    return service_account.Credentials.from_service_account_info(credentials_info)


@timingDecorator
def setDialogflowFulfillment(newUrl: str = "https://www.facebook.com"):
    dotenv.load_dotenv()
    dialogFlowCredentials = getDialogflowCredentials()
    project_id = os.environ["DIALOGFLOW_PROJECT_ID"]
    client = dialogflow_v2.FulfillmentsClient(credentials=dialogFlowCredentials)
    fulfillment = dialogflow_v2.Fulfillment()
    fulfillment.generic_web_service.uri = newUrl
    fulfillment.name = f"projects/{project_id}/locations/global/agent/fulfillment"
    mask = field_mask_pb2.FieldMask(paths=["generic_web_service.uri", "name"])

    request = dialogflow_v2.UpdateFulfillmentRequest(
        fulfillment=fulfillment,
        update_mask=mask
    )

    return client.update_fulfillment(request=request)


def __main():
    setDialogflowFulfillment()


if __name__ == "__main__":
    __main()
