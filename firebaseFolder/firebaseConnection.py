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

    def connect_to_database(self):
        # Connect to the Firebase Realtime Database
        return db.reference('/', app=self.app)

    def read_data(self, path):
        # Read data from the specified path in the database
        ref = self.connect_to_database().child(path)
        return ref.get()

    def write_data(self, path, data):
        # Write data to the specified path in the database
        ref = self.connect_to_database().child(path)
        ref.set(data)
        return True


def __main():
    fc = FirebaseConnection()
    data = fc.read_data("core_messages")
    return


if __name__ == '__main__':
    __main()
