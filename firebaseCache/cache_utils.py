import datetime
import json
import os
from pathlib import Path

from references.path_reference import getFirebaseCacheFilesPath
from utils.date_utils import timedelta_to_str

CACHE_FOLDER = getFirebaseCacheFilesPath()
SUB_CACHE_FOLDER = CACHE_FOLDER.parent


def load_cache_table():
    filepath = Path(SUB_CACHE_FOLDER, "cache_table.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file cache_table.json was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON data from cache_table.json.")
        return {}


def load_cache_json(filename: str):
    filepath = Path(CACHE_FOLDER, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            speisekarte_data = json.load(file)
        return speisekarte_data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON data from '{filename}'.")
        return {}


def save_cache_json(filename: str, data: dict):
    filepath = Path(CACHE_FOLDER, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to '{filename}'.")
    except IOError as e:
        print(f"Error: Failed to write data to '{filename}'. {str(e)}")
    except TypeError:
        print(f"Error: Provided data is not JSON serializable.")


def __main():
    aux = {'-NhgyHOQG7NkQkc3szOV': {'Autor': 'Bill',
                                    'Bebidas': [{'nome': 'Coca-cola', 'preço': 5.99, 'tamanho': '300ml'},
                                                {'nome': 'Guaraná', 'preço': 4.99, 'tamanho': '300ml'},
                                                {'nome': 'Suco de laranja', 'preço': 6.5, 'tamanho': '500ml'}],
                                    'HorárioDeFuncionamento': '17h às 22h',
                                    'Pizzas': [{'nome': 'Calabresa', 'preço': 17.5, 'tamanho': 'Grande'},
                                               {'nome': 'Frango', 'preço': 18.9, 'tamanho': 'Grande'},
                                               {'nome': 'Portuguesa', 'preço': 13.99, 'tamanho': 'Grande'},
                                               {'nome': 'Margherita', 'preço': 15.5, 'tamanho': 'Média'},
                                               {'nome': 'Quatro Queijos', 'preço': 16.9, 'tamanho': 'Grande'},
                                               {'nome': 'Pepperoni', 'preço': 19.99, 'tamanho': 'Grande'}],
                                    'Versão': '26-oct-2023'}}
    # save_cache_json("speisekarte_cache.json", aux)
    aux = load_cache_table()
    return


if __name__ == "__main__":
    __main()
