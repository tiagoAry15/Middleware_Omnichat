from flask import g as global_object

from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


def check_user_registration_from_metadata(metadata: dict):
    desired_whatsapp_number = metadata["phoneNumber"]
    all_users = get_all_users_from_global_object()
    for firebase_unique_id, user_data in all_users.items():
        if user_data["whatsappNumber"] == desired_whatsapp_number:
            return True
    return False


def get_all_users_from_global_object():
    all_users = global_object.users
    if not all_users:
        refresh_cache()
    return all_users


def refresh_cache():
    global_object.users = fetch_all_users_from_cloud_function()


def __main():
    fake_metadata = {'from': 'whatsapp', 'phoneNumber': '558599171902', 'sender': 'Mateus'}


if __name__ == '__main__':
    __main()
