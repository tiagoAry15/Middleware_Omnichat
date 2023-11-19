import asyncio
import os
import time

from api_config.core_factory import core_app
from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


class UserCacheManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.app['users'] = {}
        self.no_users_in_firebase = False

    async def get_all_users(self):
        """Fetch all users from the cache, refreshing if necessary."""
        try:
            if self.no_users_in_firebase:
                return {}
            if self.app['users']:
                return self.app['users']
            else:
                print("Refreshing cache...........")
                await self.refresh_cache()
                return self.app['users']
        except KeyError:
            print("Refreshing cache...........")
            await self.refresh_cache()
            return self.app['users']

    async def get_single_user(self, metaData: dict) -> dict or None:
        if self.no_users_in_firebase:
            return None
        desired_phone_number = metaData["phoneNumber"]
        if not self.app["users"]:
            await self.refresh_cache()
        all_users = self.app["users"]
        if not all_users:
            return None
        for unique_id, user_data in all_users.items():
            user_phone_number = user_data["phoneNumber"]
            if user_phone_number == desired_phone_number:
                return user_data
        return None

    async def check_existing_user_from_metadata(self, metaData: dict) -> bool:
        user = await self.get_single_user(metaData)
        return True if user else False

    async def refresh_cache(self):
        """Logic to refresh cache."""
        users_from_firebase = await fetch_all_users_from_cloud_function()
        if users_from_firebase:
            self.app['users'] = users_from_firebase
            self.no_users_in_firebase = False  # Reset the flag since we have users now
        else:
            self.no_users_in_firebase = True  # Set the flag to indicate no users in Firebase

    async def append_user(self, user_data: dict, unique_id: str):
        """Append a user to the global object."""
        self.no_users_in_firebase = False
        self.app["users"][unique_id] = user_data


async def main():
    user_cache_manager = UserCacheManager(core_app)
    session_metadata = {'from': ['whatsapp', '+558599171902'], 'ip': '127.0.0.1', 'phoneNumber': '558599171902',
                        'sender': 'Mateus', 'userMessage': 'Vou querer um guaraná e dois sucos de laranja'}

    # Timing the first user fetch
    start_time = time.time()
    user = await user_cache_manager.check_existing_user_from_metadata(session_metadata)
    end_time = time.time()
    print(f"First user fetch took {end_time - start_time} seconds")
    print(user)

    # Timing the second user fetch
    start_time = time.time()
    user2 = await user_cache_manager.check_existing_user_from_metadata(session_metadata)
    end_time = time.time()
    print(f"Second user fetch took {end_time - start_time} seconds")
    print(user2)


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
