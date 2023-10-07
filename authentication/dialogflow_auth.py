import os

from dotenv import load_dotenv
from google.oauth2 import service_account


def load_dialogflow_credentials():
    load_dotenv()
    credentials_dict = {
        "type": os.environ["DIALOGFLOW_TYPE"],
        "project_id": os.environ["DIALOGFLOW_PROJECT_ID"],
        "private_key_id": os.environ["DIALOGFLOW_PRIVATE_KEY_ID"],
        "private_key": os.environ["DIALOGFLOW_PRIVATE_KEY"],
        "client_email": os.environ["DIALOGFLOW_CLIENT_EMAIL"],
        "client_id": os.environ["DIALOGFLOW_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["DIALOGFLOW_CLIENT_X509_CERT_URL"],
    }
    key = credentials_dict["private_key"]
    key = key.replace("\\n", "\n")
    credentials_dict["private_key"] = key
    return service_account.Credentials.from_service_account_info(credentials_dict)


def __main():
    creds = load_dialogflow_credentials()
    return


if __name__ == '__main__':
    __main()
