import os
import pickle

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

from references.path_reference import getWebdriverPath


class TwilioScrapper:
    def __init__(self):
        load_dotenv()
        s = Service(str(getWebdriverPath()), log_output="geckodriver.log")
        self.driver = webdriver.Firefox(service=s)
        self.page_url: str = "https://www.twilio.com/login"
        self.book_links = {}
        self.characters = []
        self.webhookURL = "https://www.google.com"

    def setNewWebhookURL(self, newURL: str):
        self.webhookURL = newURL

    def run(self):
        self.__loadWebsite()

    def __loadWebsite(self):
        self.driver.get(self.page_url)
        self.driver.implicitly_wait(1)

    def __save_cookies(self):
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)

    def __load_cookies(self):
        if os.path.exists('cookies.pkl'):
            with open('cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        else:
            print("No cookie file found")


def __main():
    ts = TwilioScrapper()
    ts.run()


if __name__ == "__main__":
    __main()
