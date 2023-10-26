import json
from pathlib import Path

from firebaseCache.cache_utils import save_cache_json, load_cache_json
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
        self.cache = {}
        self.load_cache()

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("speisekarte")

    def refreshSpeisekarteCache(self) -> bool:
        all_data = self.firebaseConnection.readData()
        save_cache_json(filename="speisekarte_cache.json", data=all_data)
        return True

    def load_cache(self):
        data, timedelta = load_cache_json(filename="speisekarte_cache.json")
        if timedelta.days >= 1:
            print("Cache is outdated! Refreshing...")
            self.refreshSpeisekarteCache()
        return

    def createSpeisekarte(self, speisekarte_data: dict):
        return self.firebaseConnection.writeData(data=speisekarte_data)

    def createDummySpeisekarte(self):
        dummy_speisekarte = get_current_speisekarte()
        return self.createSpeisekarte(dummy_speisekarte)


def __main():
    fc = FirebaseConnection()
    fs = FirebaseSpeisekarte(fc)
    return


if __name__ == "__main__":
    __main()
