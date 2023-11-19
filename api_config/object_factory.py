from api_config.api_core_app_instance import core_app
from data.menu_item_handler import MenuItemHandler
from dialogflowFolder.session_manager import SessionFactory
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from firebaseFolder.firebase_speisekarte import FirebaseSpeisekarte
from firebaseFolder.firebase_user import FirebaseUser
from cache.whatsapp_user_cache import UserCacheManager
from utils.insomnia_examples import MessageConverter


menuHandler = MenuItemHandler()
dialogflowConnectionManager = SessionFactory()
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fcm = FirebaseConversation(fc)
fs = FirebaseSpeisekarte(fc)
fo = FirebaseOrder(fc)
mc = MessageConverter()
ucm = UserCacheManager(core_app)
