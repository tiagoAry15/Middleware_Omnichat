import threading
import uuid

from dialogflowFolder.dialogflow_session import DialogflowSession
from ipAddressSessions.session_manager import SessionManager


class DialogflowSessionFactory(SessionManager):
    def __init__(self):
        self.dialogflowSessions = {}
        self.lock = threading.Lock()

    def get_session(self, ip_address: str) -> DialogflowSession:
        with self.lock:
            if ip_address not in self.dialogflowSessions:
                print("Creating new dialogflow session for user: ", ip_address)
                self.dialogflowSessions[ip_address] = DialogflowSession()
            return self.dialogflowSessions[ip_address]

    def delete_session(self, ip_address: str):
        with self.lock:
            if ip_address in self.dialogflowSessions:
                del self.dialogflowSessions[ip_address]

    def delete_all_sessions(self):
        with self.lock:
            self.dialogflowSessions = {}


def __main():
    manager = DialogflowSessionFactory()
    unique_id = str(uuid.uuid4())
    user_instance: DialogflowSession = manager.get_session(unique_id)
    user_instance.initialize_session(unique_id)
    response = user_instance.getDialogFlowResponse(message="Oii")
    bot_answer = response.query_result.fulfillment_text
    print(bot_answer)


if __name__ == "__main__":
    __main()
