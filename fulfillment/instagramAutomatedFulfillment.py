from fulfillment.ngrokGetter import get_ngrok_url
from utils.decorators.time_decorator import timingDecorator
from webscrapping.instagramWebhookChanger import InstagramScrapper


@timingDecorator
def setNewInstagramWebhookCallbackURL(newUrl: str):
    ts = InstagramScrapper()
    ts.setNewWebhookURL(newURL=newUrl)
    ts.run()


def setInstagramFulfillmentNgrok():
    url = get_ngrok_url()
    setNewInstagramWebhookCallbackURL(url)
    print("Fulfillment set successfully.")


def setInstagramFulfillmentContainer():
    url = "https://flaskomnichat-xpkcivyfqq-uc.a.run.app/"
    setNewInstagramWebhookCallbackURL(url)
    print("Fulfillment set successfully.")


def __main():
    setInstagramFulfillmentNgrok()
    # setInstagramFulfillmentContainer()
    return


if __name__ == "__main__":
    __main()
