from fulfillment.ngrokGetter import get_ngrok_url
from utils.decorators.time_decorator import timingDecorator
from webscrapping.instagramWebhookChanger import TwilioScrapper


@timingDecorator
def setNewInstagramWebhookCallbackURL(newUrl: str):
    ts = TwilioScrapper()
    ts.setNewWebhookURL(newURL=newUrl)
    ts.run()


def setInstagramFulfillment():
    url = get_ngrok_url()
    setNewInstagramWebhookCallbackURL(url)
    print("Fulfillment set successfully.")


def __main():
    setInstagramFulfillment()


if __name__ == "__main__":
    __main()
