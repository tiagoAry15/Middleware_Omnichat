from dotenv import load_dotenv
from firebase_admin import credentials
from google.oauth2 import service_account

from authentication.sdk_dict import getSdkDict


def getDialogflowCredentials():
    load_dotenv()
    credentials_info = getSdkDict()
    return service_account.Credentials.from_service_account_info(credentials_info)


def getFirebaseCredentials():
    load_dotenv()
    firebase_credentials = getSdkDict()
    key = firebase_credentials["private_key"]
    key = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    key = f"-----BEGIN PRIVATE KEY-----\n{key}\n-----END PRIVATE KEY-----"
    firebase_credentials["private_key"] = key
    return credentials.Certificate(firebase_credentials)


def __main():
    creds = getFirebaseCredentials()
    return


if __name__ == '__main__':
    __main()
