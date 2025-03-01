import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService, Service

from references.path_reference import getWebdriverPath


class InstagramScrapper:
    def __init__(self):
        load_dotenv()
        s = Service(str(getWebdriverPath()), log_path=os.devnull)
        self.driver = webdriver.Firefox(service=s)
        self.page_url: str = "https://developers.facebook.com/apps/743055877386142/messenger/ig-settings/"
        self.book_links = {}
        self.characters = []
        self.webhookURL = "https://www.google.com"

    def setNewWebhookURL(self, newURL: str):
        self.webhookURL = newURL

    def run(self):
        self.__loadWebsite()
        self.__loginPipeline()
        self.__editWebhookPipeline()
        self.__closeBrowser()

    def __loadWebsite(self):
        self.driver.get(self.page_url)
        self.driver.implicitly_wait(1)

    def __loginPipeline(self):
        email_field = self.driver.find_element(By.XPATH, '//*[@id="email"]')
        password_field = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
        send_button = self.driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
        email = os.environ["INSTAGRAM_EMAIL"]
        password = os.environ["INSTAGRAM_PASSWORD"]
        email_field.send_keys(email)
        password_field.send_keys(password)
        time.sleep(0.3)
        send_button.click()
        time.sleep(0.1)

    def __editWebhookPipeline(self):
        callbackURLButtonCSS = '._3-91 > div:nth-child(1) > div:nth-child(1)'
        editCallBackURLButton = self.driver.find_element(By.CSS_SELECTOR, callbackURLButtonCSS)
        editCallBackURLButton.click()
        time.sleep(0.5)
        mainWindowXPath = "/html/body/div[4]/div[2]/div"
        mainWindow = self.driver.find_element(By.XPATH, mainWindowXPath)
        webhookFieldXPATH = (".//input[@placeholder='Validation requests and Webhook notifications for this object will"
                             " be sent to this URL.']")
        webhookField = mainWindow.find_element(By.XPATH, webhookFieldXPATH)
        webhookField.clear()
        time.sleep(0.3)
        webhookField.send_keys(self.webhookURL)
        verifyTokenXPath = (".//input[@placeholder='Token that Meta will echo back to you as part of callback URL "
                            "verification.']")
        verifyTokenTextField = mainWindow.find_element(By.XPATH, verifyTokenXPath)
        verifyTokenTextField.send_keys("Frango")
        self.driver.implicitly_wait(1)
        time.sleep(0.3)
        saveButtonXPath = '/html/body/div[4]/div[2]/div/div/div/div/div/div/div[3]/span[2]/div/div[2]/button/div/div'
        saveButton = self.driver.find_element(By.XPATH, saveButtonXPath)
        saveButton.click()
        time.sleep(1)

    def __closeBrowser(self):
        self.driver.quit()


def __main():
    ts = InstagramScrapper()
    ts.run()


if __name__ == "__main__":
    __main()
