from fulfillment.dialogflowFulfillmentSetter import setNewFulfillment
from fulfillment.ngrokGetter import get_ngrok_url


def setDialogflowFulfillment():
    url = get_ngrok_url()
    response = setNewFulfillment(newUrl=f"{url}/webhookForIntent")
    print(f"Response: {response}")
    print("Fulfillment set successfully.")


def __main():
    setDialogflowFulfillment()


if __name__ == "__main__":
    __main()
