import datetime
import json
import logging
import os
from urllib.parse import unquote
import asyncio
import requests

from api_config.api_setup import twilioClient, twilio_phone_number, twilio_fb_page_id
from firebaseFolder.firebase_conversation import FirebaseConversation
from signupBot.intent_manager import SignupBot
from api_config.object_factory import fcm
from signupBot.whatsapp_handle_new_user import handleNewWhatsappUser
from utils.dialogflow_utils import create_dialogflow_session, get_bot_response_from_session, create_signup_bot_session
from utils.helper_utils import sendTwilioResponse, extractTextFromDialogflowResponse
from utils.message_utils import convert_dialogflow_message
from utils.port_utils import get_ip_address_from_request


def updateFirebaseWithUserMessage(data: dict):
    processedData: dict = __transformTwilioDataIntoStructuredFirebaseData(data)
    userMessageJSON, phoneNumber, receivedMessage = (processedData["userMessageJSON"], processedData["phoneNumber"],
                                                     processedData["receivedMessage"])
    conversation = fcm.appendMessageToConversation(messageData=userMessageJSON, whatsappNumber=phoneNumber)
    return userMessageJSON


async def extract_data_fro_request(request):
    data = await request.post()
    print("TWILIO SANDBOX ENDPOINT!")
    unquoted_dict = {k: unquote(v) if isinstance(v, str) else v for k, v in request.headers.items()}
    dictData = {**dict(data), **unquoted_dict}
    metaData = extractMetaDataFromTwilioCall(dictData)
    metaData["ip"] = get_ip_address_from_request(request)
    userMessage = metaData["userMessage"]
    return userMessage, metaData


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


async def sendMessageToUser(message, phoneNumber: str):
    # Adiciona a mensagem ao seu sistema de gerenciamento de mensagens
    response = fcm.appendMessageToConversation(messageData=message, whatsappNumber=phoneNumber)

    # Determina o destino e a origem da mensagem com base no campo 'from'
    if message['from'] == 'whatsapp':
        destination = f'whatsapp:+{phoneNumber}'
        from_ = twilio_phone_number  # O número do Twilio para WhatsApp
    elif message['from'] == 'messenger':
        destination = f'messenger:{phoneNumber}'
        from_ = twilio_fb_page_id  # O ID da página do Twilio para o Messenger
    else:
        raise ValueError("Origem da mensagem desconhecida ou não suportada.")

    # Envia a mensagem através do Twilio
    try:
        msg = twilioClient.messages.create(
            body=message['body'],  # Assume-se que 'body' é a chave correta para o conteúdo da mensagem
            from_=from_,  # A origem da mensagem, definida acima com base no canal
            to=destination
        )
    except Exception as e:
        print(e)
        logging.error(e)
    return response


def __checkUserRegistration(phoneNumber: str):
    im = SignupBot()
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
    firebase_instance.appendMessageToConversation(messageData=message_data, whatsappNumber=phone_number)


def __handleNewUser(phoneNumber: str, receivedMessage: str):
    logging.info("Needs to sign up!")
    im = SignupBot()
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


async def appendMultipleMessagesToFirebase(userMessage: str, botAnswer: str, metaData: dict):
    return await makeHttpCallToAppendMultipleMessagesToFirebaseServerlessFunction(userMessage, botAnswer, metaData)


async def makeHttpCallToAppendMultipleMessagesToFirebaseServerlessFunction(userMessage: str, botAnswer: str,
                                                                           metaData: dict):
    payload = {
        "userMessage": userMessage,
        "botAnswer": botAnswer,
        "metaData": metaData
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = os.environ["CLOUD_FUNCTION_BASE_URL"] + "/conversation_handler/update_multiple_conversations"
    response = requests.put(url=url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error while trying to append multiple messages to Firebase: {response.text}")
    return


def create_message_json(message, metaData):
    return {
        "body": message,
        "timestamp": datetime.datetime.now().strftime('%d-%b-%Y %H:%M'),
        **metaData
    }


async def process_bot_response(existing_user, userMessage, metaData, request):
    BotResponseJSON = {
        "body": '',
        "timestamp": '',
        **metaData,
        "sender": "Bot"
    }
    ip_address = get_ip_address_from_request(request)
    metaData['userMessage'] = userMessage
    if not existing_user:
        im = create_signup_bot_session(ip_address)
        botResponse = await handleNewWhatsappUser(metaData=metaData, signupBotInstance=im)
    else:
        loop = asyncio.get_running_loop()
        session = create_dialogflow_session(ip_address)
        session.metaData = metaData
        botResponse = await loop.run_in_executor(None,
                                                 get_bot_response_from_session,
                                                 session, userMessage)

    BotResponseJSON["body"] = botResponse
    BotResponseJSON["timestamp"] = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')

    return botResponse, BotResponseJSON


def extractMetaDataFromTwilioCall(twilioDict: dict) -> dict:
    # Convert all keys to lowercase
    lower_twilioDict = {k.lower(): v for k, v in twilioDict.items()}

    # Accessing values using lowercase keys
    rawFrom = lower_twilioDict.get("from")
    sender = lower_twilioDict.get("profilename") or rawFrom.split(':')[1]
    phoneNumber = lower_twilioDict.get("waid") or rawFrom.split(':')[1]
    userMessage = lower_twilioDict.get("body")

    # Processing the 'from' value
    _from = rawFrom.split(':') if rawFrom and ':' in rawFrom else None

    return {"sender": sender, "from": _from, "phoneNumber": phoneNumber, "userMessage": userMessage}


def __main():
    pass


if __name__ == "__main__":
    __main()
