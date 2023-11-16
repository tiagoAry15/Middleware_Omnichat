import threading
import uuid

from dialogflowFolder.dialogflow_session import DialogflowSession


class DialogflowSessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def get_dialogflow_instance(self, ip_address: str) -> DialogflowSession:
        with self.lock:
            if ip_address not in self.sessions:
                print("Creating new dialogflow session for user: ", ip_address)
                self.sessions[ip_address] = DialogflowSession()
            return self.sessions[ip_address]

    def erase_session(self, user_id: str):
        with self.lock:
            if user_id in self.sessions:
                del self.sessions[user_id]


def __main():
    manager = DialogflowSessionManager()
    unique_id = str(uuid.uuid4())
    user_instance: DialogflowSession = manager.get_dialogflow_instance(unique_id)
    user_instance.initialize_session(unique_id)
    response = user_instance.getDialogFlowResponse(message="Oii")
    bot_answer = response.query_result.fulfillment_text
    print(bot_answer)


if __name__ == "__main__":
    __main()
