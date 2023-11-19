import threading
import uuid

from ipAddressSessions.session_manager import SessionManager
from signupBot.intent_manager import SignupBot
from utils.decorators.singleton_decorator import singleton


@singleton
class SignupBotFactory(SessionManager):
    def __init__(self):
        self.intentManagers = {}
        self.lock = threading.Lock()

    def get_session(self, ip_address: str) -> SignupBot:
        with self.lock:
            if ip_address not in self.intentManagers:
                print("Creating new Intent Manager for user: ", ip_address)
                self.intentManagers[ip_address] = SignupBot()
            return self.intentManagers[ip_address]

    def delete_session(self, ip_address: str):
        with self.lock:
            if ip_address in self.intentManagers:
                del self.intentManagers[ip_address]


def __main__():
    manager = SignupBotFactory()
    unique_id = str(uuid.uuid4())
    user_instance: SignupBot = manager.get_session(unique_id)
    # Initialize and use the IntentManager as needed
    # Example: intent = user_instance.determineIntent(message="Hello")


if __name__ == "__main__":
    __main__()
