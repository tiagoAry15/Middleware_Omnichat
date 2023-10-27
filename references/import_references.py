import json
from pathlib import Path

from references.path_reference import getSpeisekartePath


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
