import base64
import json
import os

from dotenv import load_dotenv
from flask import request, make_response, jsonify
from urllib.parse import parse_qs


def sendWebhookCallback(desiredMessage: str, newIntent: str = None, parameters: dict = None,
                        newContext: str = None):
    myResult = {
        "source": "dialogFlow",
        "fulfillmentText": desiredMessage
    }
    if newContext:
        myResult["outputContexts"] = [
            {
                "name": newContext,
                "lifespanCount": 1,
                "parameters": {
                    "parameter-name": "parameter-value"
                }
            }
        ]
    if newIntent:
        event = {
            "name": newIntent,
            "languageCode": "pt-BR",
            "parameters": parameters or {},
        }
        myResult["followupEventInput"] = event
    res = json.dumps(myResult, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def getDialogFlowAuth():
    load_dotenv()
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    auth_string = f"{account_sid}:{auth_token}"
    base64_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    print(base64_auth_string)


def extractDictFromBytesRequest():
    payload = request.get_data()
    stringData = payload.decode('utf-8')
    return parse_qs(stringData)


def getJsonCredentialsData() -> dict:
    dialogflowJsonFilePath = os.path.join(os.getcwd(), 'dialogflow.json')
    with open(dialogflowJsonFilePath, 'r') as f:
        return json.load(f)


def __main():
    data = getJsonCredentialsData()
    return


if __name__ == '__main__':
    __main()
