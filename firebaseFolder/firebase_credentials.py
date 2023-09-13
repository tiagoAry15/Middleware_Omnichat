import os
from firebase_admin import credentials
from dotenv import load_dotenv


def getFirebaseCredentials():
    load_dotenv()
    firebase_credentials = {
        "type": os.environ["FIREBASE_SDK_TYPE"],
        "project_id": os.environ["FIREBASE_SDK_PROJECT_ID"],
        "private_key_id": os.environ["FIREBASE_SDK_PRIVATE_KEY_ID"],
        "private_key": os.environ["FIREBASE_SDK_PRIVATE_KEY"],
        "client_email": os.environ["FIREBASE_SDK_CLIENT_EMAIL"],
        "client_id": os.environ["FIREBASE_SDK_CLIENT_ID"],
        "auth_uri": os.environ["FIREBASE_SDK_AUTH_URI"],
        "token_uri": os.environ["FIREBASE_SDK_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["FIREBASE_SDK_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["FIREBASE_SDK_CLIENT_X509_CERT_URL"]
    }
    key = firebase_credentials["private_key"]
    key = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    key = f"-----BEGIN PRIVATE KEY-----\n{key}\n-----END PRIVATE KEY-----"
    firebase_credentials["private_key"] = key
    return credentials.Certificate(firebase_credentials)


def __main():
    creds = getFirebaseCredentials()
    return


if __name__ == "__main__":
    __main()
