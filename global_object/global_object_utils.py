from flask import g as global_object


from cloudFunctionsCalls.cloud_functions_calls import fetch_all_users_from_cloud_function


async def get_all_users_from_global_object():
    from app import app
    try:

        return app['users']
    except KeyError:
        # Se não existir, atualiza o cache (faz a chamada assíncrona)
        await refresh_cache()
        return app['users']


async def refresh_cache():
    # Sua lógica para atualizar o cache vai aqui.
    from app import app
    app['users'] = await fetch_all_users_from_cloud_function()


async def append_user_to_global_object(user_data: dict, unique_id: str):
    users = await get_all_users_from_global_object()
    users[unique_id] = user_data
