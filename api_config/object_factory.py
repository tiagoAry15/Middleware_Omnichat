from data.menu_item_handler import MenuItemHandler
from ipAddressSessions.dialogflow_session_manager import DialogflowSessionFactory
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from firebaseFolder.firebase_speisekarte import FirebaseSpeisekarte
from firebaseFolder.firebase_user import FirebaseUser
from ipAddressSessions.signupBot_session_manager import SignupBotFactory
from utils.insomnia_examples import MessageConverter


menuHandler = MenuItemHandler()
dialogflowConnectionManager = DialogflowSessionFactory()
signupBotConnectionManager = SignupBotFactory()
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fcm = FirebaseConversation(fc)
fs = FirebaseSpeisekarte(fc)
fo = FirebaseOrder(fc)
mc = MessageConverter()
