import threading
import uuid

from dialogflowFolder.dialogflow_session import DialogflowSession
from signupBot.intent_manager import IntentManager


class SessionFactory:
    def __init__(self):
        self.dialogflowSessions = {}
        self.intentManagerSessions = {}
        self.lock = threading.Lock()

    def get_dialogflow_instance(self, ip_address: str) -> DialogflowSession:
        with self.lock:
            if ip_address not in self.dialogflowSessions:
                print("Creating new dialogflow session for user: ", ip_address)
                self.dialogflowSessions[ip_address] = DialogflowSession()
            return self.dialogflowSessions[ip_address]

    def get_intent_manager_instance(self, ip_address: str) -> IntentManager:
        with self.lock:
            if ip_address not in self.intentManagerSessions:
                print("Creating new Intent Manager for user: ", ip_address)
                self.intentManagerSessions[ip_address] = IntentManager()
            return self.intentManagerSessions[ip_address]

    def erase_dialogflow_session(self, ip_address: str):
        with self.lock:
            if ip_address in self.dialogflowSessions:
                del self.dialogflowSessions[ip_address]
            if ip_address in self.intentManagerSessions:
                del self.intentManagerSessions[ip_address]


def __main():
    manager = SessionFactory()
    unique_id = str(uuid.uuid4())
    user_instance: DialogflowSession = manager.get_dialogflow_instance(unique_id)
    user_instance.initialize_session(unique_id)
    response = user_instance.getDialogFlowResponse(message="Oii")
    bot_answer = response.query_result.fulfillment_text
    print(bot_answer)


if __name__ == "__main__":
    __main()
