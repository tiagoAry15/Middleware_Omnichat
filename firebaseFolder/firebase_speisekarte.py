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
        self.data = {}
        self.load_cache()

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("speisekarte")

    def refreshSpeisekarteCache(self) -> bool:
        all_data = self.firebaseConnection.readData()
        save_cache_json(filename="speisekarte_cache.json", data=all_data)
        self.data = all_data
        return True

    def load_cache(self):
        data, timedelta = load_cache_json(filename="speisekarte_cache.json")
        if timedelta.days >= 1:
            print("Cache is outdated! Refreshing...")
            self.refreshSpeisekarteCache()
        self.data = data

    def createSpeisekarte(self, speisekarte_data: dict) -> bool:
        existing = self.existing_speisekarte(speisekarte_data)
        if not existing:
            self.firebaseConnection.writeData(data=speisekarte_data)
            return True
        return False

    def createDummySpeisekarte(self):
        dummy_speisekarte = get_current_speisekarte()
        return self.createSpeisekarte(dummy_speisekarte)

    def existing_speisekarte(self, input_speisekarte: dict) -> bool:
        speisekarte_pool = list(self.data.values())
        return input_speisekarte in speisekarte_pool

    def read_speisekarte(self, author: str) -> dict or None:
        speisekarte_pool = list(self.data.values())
        for item in speisekarte_pool:
            item_author = item["Autor"].lower()
            if item_author == author.lower():
                return item
        return None

    def update_speisekarte(self, author: str, **kwargs) -> bool or None:
        speisekarte = self.read_speisekarte(author=author)
        if not speisekarte:
            return None
        for key, value in kwargs.items():
            speisekarte[key] = value
        self.firebaseConnection.overWriteData(data=speisekarte)
        return True

    def delete_speisekarte(self, author: str):
        # TODO
        speisekarte = self.read_speisekarte(author=author)
        if not speisekarte:
            return None
        self.firebaseConnection.deleteData(path="", data=speisekarte)
        return True


def __main():
    fc = FirebaseConnection()
    fs = FirebaseSpeisekarte(fc)
    speisekarte = get_current_speisekarte()
    fs.delete_speisekarte("bill")
    return


if __name__ == "__main__":
    __main()
