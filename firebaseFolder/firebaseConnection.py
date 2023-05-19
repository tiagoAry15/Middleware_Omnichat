import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db

from references.pathReference import getFirebaseSDKPath


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


def __main():
    fc = FirebaseConnection()
    data = fc.readData("core_messages")
    return


if __name__ == '__main__':
    __main()
