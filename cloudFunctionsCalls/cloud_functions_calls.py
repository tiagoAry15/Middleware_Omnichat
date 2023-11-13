import os
import aiohttp

# Suponha que as variáveis de ambiente sejam definidas como CLOUD_FUNCTION_BASE_URL
CLOUD_FUNCTION_BASE_URL = os.environ.get('CLOUD_FUNCTION_BASE_URL')


async def register_user_on_firebase(user_details: dict):
    url = f'{CLOUD_FUNCTION_BASE_URL}/user_handler/create'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=user_details) as response:
            return await response.json()  # Retornar o JSON da resposta


async def fetch_all_users_from_cloud_function():
    url = f'{CLOUD_FUNCTION_BASE_URL}/user_handler/read'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                return await response.json()  # Retornar o JSON da resposta
    except Exception as e:
        print(e)
        return {'error': str(e)}
