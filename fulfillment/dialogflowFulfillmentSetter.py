import os
import dotenv
from google.cloud import dialogflow_v2
from google.protobuf import field_mask_pb2

from authentication.credentials_loader import getDialogflowCredentials
from utils.decorators.time_decorator import timingDecorator


@timingDecorator
def setDialogflowFulfillment(newUrl: str = "https://www.facebook.com"):
    dotenv.load_dotenv()
    dialogFlowCredentials = getDialogflowCredentials()
    project_id = os.environ["SDK_PROJECT_ID"]
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
