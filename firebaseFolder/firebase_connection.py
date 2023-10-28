import os
from typing import Any

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import db
from utils.decorators.singleton_decorator import singleton
from authentication.credentials_loader import getFirebaseCredentials


@singleton
class FirebaseConnection:
    def __init__(self):
        """ FirebaseConnection is a singleton class that provides mechanisms for interacting with
        Firebase realtime database."""
        load_dotenv()
        cred = getFirebaseCredentials()
        database_url = os.environ["FIREBASE_DATABASE_URL"]
        self.app = firebase_admin.initialize_app(cred, {"databaseURL": database_url})
        self.connection = db.reference('/', app=self.app)

    def changeDatabaseConnection(self, path: str) -> db.reference:
        """Change the current active reference to another in Firebase."""
        self.connection = db.reference(f'/{path}', app=self.app)

    def readData(self, path: str = None) -> db.reference:
        """Reads and returns data from Firebase at the specified path."""
        ref = self.connection.child(path) if path is not None else self.connection
        return ref.get()

    def getValue(self, path: str) -> Any:
        """Get a value from Firebase at the specified path."""
        return self.readData(path)

    def setValue(self, path: str, value: Any) -> bool:
        """Set a value in Firebase at the specified path."""
        self.connection.child(path).set(value)
        return True

    def writeData(self, path: str = None, data: dict = None):
        """Writes data to Firebase at the specified path."""
        if data is None:
            data = {"dummyData": 5}
        ref = self.connection.child(path) if path is not None else self.connection
        new_ref = ref.push(data)
        return new_ref.key

    def writeDataWithoutUniqueId(self, path: str = None, data: dict = None) -> bool:
        """Writes data to Firebase at the specified path."""
        if data is None:
            data = {"dummyData": 5}

        # If a path is provided, write data to that path.
        # If no path is provided, write data to the root.
        ref = self.connection.child(path) if path else self.connection

        # Use set method instead of push to avoid Firebase's unique ID generation.
        ref.set(data)
        return True

    def overWriteData(self, path: str = None, data=None) -> bool:
        """Overwrites data at the specified path in Firebase."""
        if data is None:
            data = {"dummyData": 5}
        ref = self.connection.child(path) if path is not None else self.connection
        ref.set(data)
        return True

    def deleteData(self, path: str) -> bool:
        """Deletes data at the specified path in Firebase."""
        ref = self.connection.child(path)
        ref.delete()
        return True

    def deleteAllData(self) -> bool:
        """Deletes all data at the root of the Firebase Database."""
        ref = self.connection
        ref.delete()
        return True

    def getUniqueIdByData(self, path: str = None, data=None) -> str:
        """Returns the generated unique key for that data."""
        if data is None:
            raise ValueError("Data cannot be None")
        ref = self.connection.child(path) if path is not None else self.connection
        return ref.push(data).key


def __main():
    fc = FirebaseConnection()
    data = fc.readData("users")
    return


if __name__ == '__main__':
    __main()
