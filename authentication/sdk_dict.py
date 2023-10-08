import os


def getSdkDict():
    return {
        "type": os.environ["SDK_TYPE"],
        "project_id": os.environ["SDK_PROJECT_ID"],
        "private_key_id": os.environ["SDK_PRIVATE_KEY_ID"],
        "private_key": os.environ["SDK_PRIVATE_KEY"].replace("\\n", "\n").strip(),
        "client_email": os.environ["SDK_CLIENT_EMAIL"],
        "client_id": os.environ["SDK_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["SDK_CLIENT_X509_CERT_URL"]
    }
