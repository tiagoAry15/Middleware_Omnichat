import asyncio
import os

from api_config.api_core_app import core_app
from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


async def initialize_cache():
    """Initial cache loading at the start of the application."""
    print("Initializing cache")
    core_app['users'] = await fetch_all_users_from_cloud_function()


async def get_all_users_from_global_object():
    """Fetch all users from the cache, refreshing if necessary."""
    try:
        if core_app['users']:
            return core_app['users']
        else:
            await refresh_cache()
            return core_app['users']
    except KeyError as e:
        await refresh_cache()
        return core_app['users']


async def get_single_user_from_global_object(address: str, cpf: str, name: str, phoneNumber: str):
    desired_user_data = {"address": address, "cpf": cpf, "name": name, "phoneNumber": phoneNumber}
    try:
        all_users = core_app["users"]
    except KeyError as e:
        await refresh_cache()
        all_users = core_app["users"]
    for unique_id, user_data in all_users.items():
        if user_data == desired_user_data:
            return user_data


async def refresh_cache():
    """Logic to refresh cache."""
    core_app['users'] = await fetch_all_users_from_cloud_function()


async def append_user_to_global_object(user_data: dict, unique_id: str):
    """Append a user to the global object."""
    users = await get_all_users_from_global_object()
    users[unique_id] = user_data


async def __main():
    # users = await get_all_users_from_global_object()
    # print(users)
    user = await get_single_user_from_global_object(address="rua marcos macedo 700",
                                                    cpf='06354761345',
                                                    name='Tiago',
                                                    phoneNumber='558599663533')
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
