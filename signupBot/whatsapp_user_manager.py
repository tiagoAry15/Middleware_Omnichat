import asyncio
import os
import time
from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


class UserCacheManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.app['users'] = {}

    async def initialize_cache(self):
        """Initial cache loading at the start of the application."""
        print("Initializing cache")
        self.app['users'] = await fetch_all_users_from_cloud_function()

    async def get_all_users(self):
        """Fetch all users from the cache, refreshing if necessary."""
        try:
            if self.app['users']:
                return self.app['users']
            else:
                await self.refresh_cache()
                return self.app['users']
        except KeyError:
            await self.refresh_cache()
            return self.app['users']

    async def get_single_user(self, address: str, cpf: str, name: str, phoneNumber: str):
        desired_user_data = {"address": address, "cpf": cpf, "name": name, "phoneNumber": phoneNumber}
        if not self.app["users"]:
            await self.refresh_cache()
        try:
            all_users = self.app["users"]
        except KeyError:
            await self.refresh_cache()
            all_users = self.app["users"]

        for unique_id, user_data in all_users.items():
            if user_data == desired_user_data:
                return user_data

    async def refresh_cache(self):
        """Logic to refresh cache."""
        self.app['users'] = await fetch_all_users_from_cloud_function()

    async def append_user(self, user_data: dict, unique_id: str):
        """Append a user to the global object."""
        users = await self.get_all_users()
        users[unique_id] = user_data


async def main():
    user_cache_manager = UserCacheManager()

    # Timing the first user fetch
    start_time = time.time()
    user = await user_cache_manager.get_single_user(address="rua marcos macedo 700",
                                                    cpf='06354761345',
                                                    name='Tiago',
                                                    phoneNumber='558599663533')
    end_time = time.time()
    print(f"First user fetch took {end_time - start_time} seconds")
    print(user)

    # Timing the second user fetch
    start_time = time.time()
    user2 = await user_cache_manager.get_single_user(address="rua marcos macedo 700",
                                                     cpf='06354761345',
                                                     name='Tiago',
                                                     phoneNumber='558599663533')
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
