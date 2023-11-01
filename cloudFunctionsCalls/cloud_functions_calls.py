import requests


def register_user_on_firebase(user_details: dict):
    url = 'https://us-central1-pizzadobill-rpin.cloudfunctions.net/user_handler/read'
    body = user_details
    return requests.post(url=url, json=body)


def fetch_all_users_from_cloud_function():
    url = 'https://us-central1-pizzadobill-rpin.cloudfunctions.net/user_handler/read'
    return requests.get(url=url).json()
