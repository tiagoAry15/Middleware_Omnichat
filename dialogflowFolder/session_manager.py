from abc import ABC, abstractmethod


class SessionManager(ABC):

    @abstractmethod
    def get_session(self, ip_address: str):
        pass

    @abstractmethod
    def delete_session(self, ip_address: str):
        pass
