from flask import g as global_object

from api_config.api_config import app
from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


def get_all_users_from_global_object():
    with app.app_context():
        try:
            return global_object.users
        except AttributeError:
            refresh_cache()
            return global_object.users


def refresh_cache():
    global_object.users = fetch_all_users_from_cloud_function()


def append_user_to_global_object(user_data: dict, unique_id: str):
    users = get_all_users_from_global_object()
    users[unique_id] = user_data
