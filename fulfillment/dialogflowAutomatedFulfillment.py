from fulfillment.dialogflowFulfillmentSetter import setDialogflowFulfillment
from fulfillment.ngrokGetter import get_ngrok_url


def setDialogflowFulfillment():
    url = get_ngrok_url()
    response = setDialogflowFulfillment(newUrl=f"{url}/webhookForIntent")
    print(f"Response: {response}")
    print("Fulfillment set successfully.")


def __main():
    setDialogflowFulfillment()


if __name__ == "__main__":
    __main()
