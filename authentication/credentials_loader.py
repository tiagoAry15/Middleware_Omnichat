from dotenv import load_dotenv
from firebase_admin import credentials
from google.oauth2 import service_account

from authentication.sdk_dict import getSdkDict


def sanitize_sdk_dict(sdk_dict: dict) -> dict:
    key = sdk_dict["private_key"]
    key = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    key = f"-----BEGIN PRIVATE KEY-----\n{key}\n-----END PRIVATE KEY-----"
    sdk_dict["private_key"] = key
    return sdk_dict


def getDialogflowCredentials():
    load_dotenv()
    credentials_info = getSdkDict()
    credentials_info = sanitize_sdk_dict(credentials_info)
    return service_account.Credentials.from_service_account_info(credentials_info)


def getFirebaseCredentials():
    load_dotenv()
    firebase_credentials = getSdkDict()
    firebase_credentials = sanitize_sdk_dict(firebase_credentials)
    return credentials.Certificate(firebase_credentials)


def __main():
    creds = getDialogflowCredentials()
    return


if __name__ == '__main__':
    __main()
