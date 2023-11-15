from api_config.api_core_app import core_app
from data.menu_item_handler import MenuItemHandler
from dialogflowFolder.session_manager import SessionManager
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from firebaseFolder.firebase_speisekarte import FirebaseSpeisekarte
from firebaseFolder.firebase_user import FirebaseUser
from signupBot.whatsapp_user_manager import UserCacheManager
from utils.insomnia_examples import MessageConverter


menuHandler = MenuItemHandler()
dialogflowConnectionManager = SessionManager()
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fcm = FirebaseConversation(fc)
fs = FirebaseSpeisekarte(fc)
fo = FirebaseOrder(fc)
mc = MessageConverter()
ucm = UserCacheManager(core_app)
