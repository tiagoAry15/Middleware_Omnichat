from fulfillment.dialogflowFulfillmentSetter import setDialogflowFulfillment
from fulfillment.instagramAutomatedFulfillment import setNewInstagramWebhookCallbackURL
from fulfillment.ngrokGetter import get_ngrok_url


def fulfillmentPipeline():
    url = get_ngrok_url()
    response = setDialogflowFulfillment(newUrl=f"{url}/webhookForIntent")
    setNewInstagramWebhookCallbackURL(newUrl=f"{url}/instagram")
    return


def __main():
    fulfillmentPipeline()


if __name__ == "__main__":
    __main()
