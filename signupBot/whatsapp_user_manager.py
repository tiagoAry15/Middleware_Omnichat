from global_object.global_object_utils import get_all_users_from_global_object


async def check_existing_user_from_metadata(metadata: dict):
    desired_whatsapp_number = metadata["phoneNumber"]
    all_users = await get_all_users_from_global_object()
    if all_users is None or all_users == []:
        return False
    for firebase_unique_id, user_data in all_users.items():
        if user_data["phoneNumber"] == desired_whatsapp_number:
            return True
    return False


def __main():
    fake_metadata = {'from': 'whatsapp', 'phoneNumber': '558599171902', 'sender': 'Mateus'}


if __name__ == '__main__':
    __main()
