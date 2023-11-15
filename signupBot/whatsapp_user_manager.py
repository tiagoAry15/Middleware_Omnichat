import asyncio
import os
import sys

from dialogflowFolder.dialogflow_session import DialogflowSession
from global_object.global_object_utils import get_all_users_from_global_object
from utils.dialogflow_utils import create_session


async def check_existing_user_from_metadata(metadata: dict):
    user = await __get_user_from_metadata(metadata)
    if user is None:
        return False
    else:
        session: DialogflowSession = create_session(metadata["ip"])
        session.metaData = metadata
        return True


async def __get_user_from_metadata(metadata: dict):
    desired_whatsapp_number = metadata["phoneNumber"]
    all_users = await get_all_users_from_global_object()
    if all_users is None or all_users == []:
        return None
    for firebase_unique_id, user_data in all_users.items():
        if user_data["phoneNumber"] == desired_whatsapp_number:
            return user_data
    return None


async def __main():
    fake_metadata = {'from': 'whatsapp', 'phoneNumber': '558599171902', 'sender': 'Mateus', 'ip': '127.0.0.1',
                     'userMessage': 'oiiii'}
    user = await __get_user_from_metadata(fake_metadata)
    print(user)
    return


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(__main())
    finally:
        loop.close()
