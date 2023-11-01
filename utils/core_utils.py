import datetime
import json
import logging
import requests
from firebaseFolder.firebase_conversation import FirebaseConversation
from signupBot.intent_manager import IntentManager
from api_config.object_factory import fcm
from utils.helper_utils import sendTwilioResponse, extractTextFromDialogflowResponse
from utils.message_utils import convert_dialogflow_message


def updateFirebaseWithUserMessage(data: dict):
    processedData: dict = __transformTwilioDataIntoStructuredFirebaseData(data)
    userMessageJSON, phoneNumber, receivedMessage = (processedData["userMessageJSON"], processedData["phoneNumber"],
                                                     processedData["receivedMessage"])
    conversation = fcm.appendMessageToWhatsappNumber(messageData=userMessageJSON, whatsappNumber=phoneNumber)
    return userMessageJSON


def __transformTwilioDataIntoStructuredFirebaseData(data: dict) -> dict:
    currentTime = datetime.datetime.now().strftime('%H:%M')
    return {
        'phoneNumber': data['WaId'][0],
        'receivedMessage': data['Body'][0],
        'userMessageJSON': {
            'body': data['Body'][0],
            'from': 'whatsapp',
            'phoneNumber': data['WaId'][0],
            'sender': data['ProfileName'][0],
            'time': currentTime
        }
    }


def __checkUserRegistration(phoneNumber: str):
    im = IntentManager()
    needsToSignUp = not im.existingWhatsapp(phoneNumber)
    return needsToSignUp


def processDialogFlowMessage(messageData: dict):
    phoneNumber = messageData["phoneNumber"]
    receivedMessage = messageData["body"]
    needsToSignUp = __checkUserRegistration(phoneNumber)
    if needsToSignUp:
        output, dialogflowResponseJSON = __handleNewUser(phoneNumber, receivedMessage)
    else:
        output, dialogflowResponseJSON = __handleExistingUser(phoneNumber, receivedMessage)
    storeMessageInFirebase(firebase_instance=fcm, message_data=output, phone_number=phoneNumber)
    return dialogflowResponseJSON


def storeMessageInFirebase(firebase_instance: FirebaseConversation, message_data: dict, phone_number: str):
    firebase_instance.appendMessageToWhatsappNumber(messageData=message_data, whatsappNumber=phone_number)


def __handleNewUser(phoneNumber: str, receivedMessage: str):
    logging.info("Needs to sign up!")
    im = IntentManager()
    im.extractedParameters["phoneNumber"] = phoneNumber
    botAnswer = im.twilioSingleStep(receivedMessage)
    dialogflowResponseJSON = convert_dialogflow_message(botAnswer, phoneNumber)
    output = {
        "body": botAnswer,
        "formattedBody": sendTwilioResponse(body=botAnswer),
        "sender": "Bot"
    }
    return output, dialogflowResponseJSON


def __handleExistingUser(phoneNumber: str, receivedMessage: str):
    logging.info("Already signup!")
    dialogflowResponse = dialogflowConnection.getDialogFlowResponse(receivedMessage)
    botDialogflowResponseJSON = convert_dialogflow_message(dialogflowResponse.query_result.fulfillment_text,
                                                           phoneNumber)
    output = {
        "body": dialogflowResponse.query_result.fulfillment_text,
        "formattedBody": extractTextFromDialogflowResponse(dialogflowResponse),
        "sender": "Bot"
    }
    return output, botDialogflowResponseJSON


def appendMultipleMessagesToFirebase(userMessage: str, botAnswer: str, metaData: dict):
    return makeHttpCallToAppendMultipleMessagesToFirebaseServerlessFunction(userMessage, botAnswer, metaData)


def makeHttpCallToAppendMultipleMessagesToFirebaseServerlessFunction(userMessage: str, botAnswer: str, metaData: dict):
    payload = {
        "userMessage": userMessage,
        "botAnswer": botAnswer,
        "metaData": metaData
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://us-central1-pizzadobill-rpin.cloudfunctions.net/update_multiple_conversations"
    return requests.post(url=url, headers=headers, json=payload)


def extractMetaDataFromTwilioCall(twilioDict: dict) -> dict:
    sender = twilioDict["ProfileName"][0]
    rawFrom = twilioDict["From"]
    _from = rawFrom[0].split(':')[0] if rawFrom and ':' in rawFrom[0] else None
    phoneNumber = twilioDict["WaId"][0]
    userMessage = twilioDict["Body"][0]
    return {"sender": sender, "from": _from, "phoneNumber": phoneNumber, "userMessage": userMessage}


def __main():
    pass


if __name__ == "__main__":
    __main()
