import requests


def register_user_on_firebase(user_details: dict):
    url = 'https://us-central1-pizzadobill-rpin.cloudfunctions.net/user_handler/create'
    body = user_details
    response = requests.post(url=url, json=body)
    return response


def fetch_all_users_from_cloud_function():
    url = 'https://us-central1-pizzadobill-rpin.cloudfunctions.net/user_handler/read'
    return requests.get(url=url).json()
