import os

from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dialogflow_session import DialogFlowSession
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_user import FirebaseUser
from message_converter import MessageConverter

load_dotenv()
twilio_account_ssid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
twilioClient = Client(twilio_account_ssid, twilio_auth_token)
app = Flask(__name__)
originList = ["http://localhost:5173", "https://dbc1-187-18-142-212.ngrok-free.app"]
CORS(app, support_credentials=True)
socketInstance = SocketIO(app, cors_allowed_origins=originList)
dialogFlowInstance = DialogFlowSession()
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fcm = FirebaseConversation(fc)
mc = MessageConverter()


@app.before_first_request
def before_first_request():
    print("API loaded!")


def __main():
    app.run(port=4000, host="0.0.0.0")
    print("API loaded!")


if __name__ == '__main__':
    __main()
