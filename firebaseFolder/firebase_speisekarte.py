import datetime

from firebaseCache.cache_utils import save_cache_json, load_cache_json, load_cache_table
from firebaseFolder.firebase_cache import cache_create, cache_update, cache_delete
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from references.import_references import get_current_speisekarte
from utils.decorators.singleton_decorator import singleton


@singleton
class FirebaseSpeisekarte(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection
        self.cache_file = "speisekarte_cache.json"
        self.data = {}
        self._load_cache()

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("speisekarte")

    def refreshSpeisekarteCache(self) -> bool:
        all_data = self.firebaseConnection.readData()
        save_cache_json(filename="speisekarte_cache.json", data=all_data)
        self.data = all_data
        return True

    def _load_cache(self):
        filename = self.cache_file
        cache_table = load_cache_table()
        cache_last_update = cache_table[filename]
        today = datetime.date.today().strftime("%d-%b-%Y")
        timedelta = datetime.datetime.strptime(today, "%d-%b-%Y") - datetime.datetime.strptime(cache_last_update,
                                                                                               "%d-%b-%Y")
        if timedelta.days >= 1:
            print("Cache is outdated! Refreshing...")
            self.refreshSpeisekarteCache()
            cache_table[filename] = today
            save_cache_json(filename="..\\cache_table.json", data=cache_table)
        self.data = load_cache_json(filename=filename)

    def save_cache(self):
        save_cache_json(filename="speisekarte_cache.json", data=self.data)
        return True

    def existing_speisekarte(self, input_speisekarte: dict) -> bool:
        speisekarte_pool = list(self.data.values())
        return input_speisekarte in speisekarte_pool

    def createDummySpeisekarte(self):
        dummy_speisekarte = get_current_speisekarte()
        return self.createSpeisekarte(dummy_speisekarte)

    def _get_unique_id_by_author(self, author: str) -> str or None:
        speisekarte_pool = list(self.data.keys())
        for unique_id in speisekarte_pool:
            item = self.data[unique_id]
            item_author = item["Autor"].lower()
            if item_author == author.lower():
                return unique_id
        return None

    @cache_create
    def createSpeisekarte(self, speisekarte_data: dict) -> bool:
        existing = self.existing_speisekarte(speisekarte_data)
        if not existing:
            return True
        print("Speisekarte already exists!")
        return False

    def read_speisekarte(self, author: str) -> dict or None:
        speisekarte_pool = list(self.data.values())
        for item in speisekarte_pool:
            item_author = item["Autor"].lower()
            if item_author == author.lower():
                return item
        return None

    @cache_update
    def update_speisekarte(self, author: str, newData: dict) -> bool or None:
        speisekarte = self.read_speisekarte(author)
        for key, value in newData.items():
            speisekarte[key] = value
        self.firebaseConnection.overWriteData(data=speisekarte)
        return True

    @cache_delete
    def delete_speisekarte(self, author: str):
        speisekarte_unique_id = self._get_unique_id_by_author(author=author)
        if not speisekarte_unique_id:
            return None
        self.firebaseConnection.deleteData(path=speisekarte_unique_id)
        return True


def __main():
    fc = FirebaseConnection()
    fs = FirebaseSpeisekarte(fc)
    # speisekarte = get_current_speisekarte()
    # fs.createDummySpeisekarte()
    # fs.update_speisekarte("Bill", {"HorárioDeFuncionamento": "17 às 23h"})
    fs.delete_speisekarte("Bill")
    # fs.refreshSpeisekarteCache()
    return


if __name__ == "__main__":
    __main()
