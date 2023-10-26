import json
from pathlib import Path

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from references.path_reference import getSpeisekartePath
from utils.decorators.singleton_decorator import singleton


def get_current_speisekarte() -> dict:
    file_path = getSpeisekartePath()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            speisekarte_data = json.load(file)
        return speisekarte_data
    except FileNotFoundError:
        print(f"Error: The file '{Path(file_path).name}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON data from '{Path(file_path).name}'.")
        return {}


@singleton
class FirebaseSpeisekarte(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("speisekarte")

    def createSpeisekarteCache(self):
        pass

    def getAllSpeisekarte(self):
        return self.firebaseConnection.readData()

    def createSpeisekarte(self, speisekarte_data: dict):
        return self.firebaseConnection.writeData(data=speisekarte_data)

    def createDummySpeisekarte(self):
        dummy_speisekarte = get_current_speisekarte()
        return self.createSpeisekarte(dummy_speisekarte)


def __main():
    fc = FirebaseConnection()
    fs = FirebaseSpeisekarte(fc)
    all_speisekarte = fs.getAllSpeisekarte()
    return


if __name__ == "__main__":
    __main()
