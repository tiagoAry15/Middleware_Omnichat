import datetime

from firebaseCache.cache_utils import save_cache_json, load_cache_json, load_cache_table
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

    def _refreshSpeisekarteCache(self) -> bool:
        self.firebaseConnection.changeDatabaseConnection("speisekarte")
        all_data = self.firebaseConnection.readData()
        if all_data is None:
            template = get_current_speisekarte()
            unique_id = self.firebaseConnection.writeData(data=template)
            all_data = {unique_id: template}
        save_cache_json(filename="speisekarte_cache.json", data=all_data)
        self.data = all_data
        return True

    def _load_cache(self):
        filename = self.cache_file
        cache_table = load_cache_table()
        cache_last_update = cache_table[filename]
        timestamp_format = "%d-%b-%Y at %H:%M"
        today = datetime.datetime.now().strftime(timestamp_format)
        timedelta = datetime.datetime.strptime(today, timestamp_format) - datetime.datetime.strptime(cache_last_update,
                                                                                                     timestamp_format)
        days_difference = timedelta.days
        if days_difference >= 1:
            print("Cache is outdated! Refreshing...")
            self._refreshSpeisekarteCache()
            cache_table[filename] = today
            save_cache_json(filename="..\\cache_table.json", data=cache_table)
        self.data = load_cache_json(filename=filename)

    def _save_cache(self):
        save_cache_json(filename="speisekarte_cache.json", data=self.data)
        return True

    def _get_firebase_unique_id_by_author(self, author: str) -> str or None:
        speisekarte_pool = list(self.data.keys())
        for unique_id in speisekarte_pool:
            item = self.data[unique_id]
            item_author = item["Autor"].lower()
            if item_author == author.lower():
                return unique_id
        return None

    def createDummySpeisekarte(self):
        dummy_speisekarte = get_current_speisekarte()
        return self.createSpeisekarte(dummy_speisekarte)

    def createSpeisekarte(self, speisekarte_data: dict) -> bool:
        author = speisekarte_data["Autor"]
        cache_unique_id = self._get_firebase_unique_id_by_author(author)
        if cache_unique_id:
            return True
        firebase_unique_id = self.firebaseConnection.writeData(data=speisekarte_data)
        self.data[firebase_unique_id] = speisekarte_data
        self._save_cache()
        return False

    def read_speisekarte(self, author: str) -> dict or None:
        firebase_unique_id = self._get_firebase_unique_id_by_author(author)
        if firebase_unique_id not in self.data.keys():
            return None
        return self.data[firebase_unique_id]

    def update_speisekarte(self, author: str, newData: dict) -> bool or None:
        firebase_unique_id = self._get_firebase_unique_id_by_author(author)
        if not firebase_unique_id:
            return False
        speisekarte = self.data[firebase_unique_id]
        for key, value in newData.items():
            speisekarte[key] = value
        speisekarte['Versão'] = datetime.datetime.now().strftime("%d-%b-%Y")
        self.firebaseConnection.overWriteData(data=speisekarte)
        self._save_cache()
        return speisekarte

    def delete_speisekarte(self, author: str):
        speisekarte_unique_id = self._get_firebase_unique_id_by_author(author=author)
        if not speisekarte_unique_id:
            return None
        self.firebaseConnection.deleteData(path=speisekarte_unique_id)
        del self.data[speisekarte_unique_id]
        self._save_cache()
        return True


def __main():
    fc = FirebaseConnection()
    fs = FirebaseSpeisekarte(fc)
    # speisekarte = get_current_speisekarte()
    fs.createDummySpeisekarte()
    # fs.update_speisekarte("Bill", {"HorárioDeFuncionamento": "17 às 23h"})
    # fs.delete_speisekarte("Bill")
    return


if __name__ == "__main__":
    __main()
