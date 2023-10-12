import os

from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO as FlaskSocketIO

from data.speisekarte_loader import SpeisekarteObject
from dialogflowFolder.dialogflow_session import DialogflowSession
from data.menu_item_handler import MenuItemHandler
from dialogflowFolder.session_manager import SessionManager
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_user import FirebaseUser
from utils.insomnia_examples import MessageConverter

load_dotenv()
twilio_account_ssid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
twilioClient = Client(twilio_account_ssid, twilio_auth_token)

menuHandler = MenuItemHandler()
dialogflowConnectionManager = SessionManager()
speisekarteInstance = SpeisekarteObject()
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fcm = FirebaseConversation(fc)
mc = MessageConverter()
app = Flask(__name__)

originList = ["http://localhost:5173", "https://dbc1-187-18-142-212.ngrok-free.app"]
CORS(app, support_credentials=True, origins='*')
socketio = FlaskSocketIO(app, cors_allowed_origins='*')


@app.route('/')
def hello():
    return 'Hello, World!', 200


def __main():
    print("API loaded!")
    socketio.run(app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    __main()
