import asyncio
import os

from api_config.api_config import app
from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


async def get_all_users_from_global_object():
    try:
        if app['users']:
            return app['users']
        else:
            await refresh_cache()
            return app['users']
    except KeyError as e:
        await refresh_cache()
        return app['users']


async def refresh_cache():
    # Sua lógica para atualizar o cache vai aqui.
    app['users'] = await fetch_all_users_from_cloud_function()


async def append_user_to_global_object(user_data: dict, unique_id: str):
    users = await get_all_users_from_global_object()
    users[unique_id] = user_data


async def __main():
    users = await get_all_users_from_global_object()
    print(users)
    return


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(__main())
    finally:
        loop.close()
