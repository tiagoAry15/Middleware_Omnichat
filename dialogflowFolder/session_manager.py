import threading

from dialogflowFolder.dialogflow_session import DialogflowSession


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def get_instance_session(self, user_id: str) -> DialogflowSession:
        with self.lock:
            if user_id not in self.sessions:
                self.sessions[user_id] = DialogflowSession()
            return self.sessions[user_id]
