import os


def getFirebaseDict():
    return {
        "type": os.environ["FIREBASE_SDK_TYPE"],
        "project_id": os.environ["FIREBASE_SDK_PROJECT_ID"],
        "private_key_id": os.environ["FIREBASE_SDK_PRIVATE_KEY_ID"],
        "private_key": os.environ["FIREBASE_SDK_PRIVATE_KEY"].replace("\\n", "\n").strip(),
        "client_email": os.environ["FIREBASE_SDK_CLIENT_EMAIL"],
        "client_id": os.environ["FIREBASE_SDK_CLIENT_ID"],
        "auth_uri": os.environ["FIREBASE_SDK_AUTH_URI"],
        "token_uri": os.environ["FIREBASE_SDK_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["FIREBASE_SDK_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["FIREBASE_SDK_CLIENT_X509_CERT_URL"]
    }


def getDialogflowDict():
    return {
        "type": os.environ["DIALOGFLOW_TYPE"],
        "project_id": os.environ["DIALOGFLOW_PROJECT_ID"],
        "private_key_id": os.environ["DIALOGFLOW_PRIVATE_KEY_ID"],
        "private_key": os.environ["DIALOGFLOW_PRIVATE_KEY"].replace("\\n", "\n").strip(),
        "client_email": os.environ["DIALOGFLOW_CLIENT_EMAIL"],
        "client_id": os.environ["DIALOGFLOW_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["DIALOGFLOW_CLIENT_X509_CERT_URL"]
    }
