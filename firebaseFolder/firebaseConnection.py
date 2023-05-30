import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db

from dialogFlowSession import singleton
from references.pathReference import getFirebaseSDKPath


@singleton
class FirebaseConnection:
    def __init__(self):
        load_dotenv()
        cred = credentials.Certificate(getFirebaseSDKPath())
        self.app = firebase_admin.initialize_app(cred, {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")})
        self.connection = db.reference('/', app=self.app)

    def changeDatabaseConnection(self, path: str) -> db.reference:
        self.connection = db.reference(f'/{path}', app=self.app)

    def readData(self, path: str = None) -> db.reference:
        ref = self.connection.child(path) if path is not None else self.connection
        return ref.get()

    def writeData(self, path: str = None, data=None) -> bool:
        if data is None:
            data = {"dummyData": 5}
        ref = self.connection.child(path) if path is not None else self.connection
        ref.push(data)
        return True

    def overWriteData(self, path: str = None, data=None) -> bool:
        if data is None:
            data = {"dummyData": 5}
        ref = self.connection.child(path) if path is not None else self.connection
        ref.set(data)
        return True

    def deleteData(self, path: str = None, data=None) -> bool:
        user_id = self.getUniqueIdByData(path, data)
        if user_id is None:
            raise ValueError("User ID cannot be None")
        ref = self.connection.child(path) if path is not None else self.connection
        user_ref = ref.child(user_id)
        user_ref.delete()
        return True

    def getUniqueIdByData(self, path: str = None, data=None):
        if data is None:
            raise ValueError("Data cannot be None")
        ref = self.connection.child(path) if path is not None else self.connection
        return ref.push(data).key


def __main():
    fc = FirebaseConnection()
    data = fc.deleteData("users", {"email": "user@example.com", "password": "password"})
    return


if __name__ == '__main__':
    __main()
