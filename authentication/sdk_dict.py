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
        "auth_uri": os.environ["DIALOGFLOW_AUTH_URI"],
        "token_uri": os.environ["DIALOGFLOW_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["DIALOGFLOW_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["DIALOGFLOW_CLIENT_X509_CERT_URL"]
    }
