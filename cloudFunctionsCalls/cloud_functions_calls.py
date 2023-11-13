import os
import aiohttp
import asyncio

from dotenv import load_dotenv

load_dotenv()
CLOUD_FUNCTION_BASE_URL = os.environ.get('CLOUD_FUNCTION_BASE_URL')


async def register_user_on_firebase(user_details: dict):
    url = f'{CLOUD_FUNCTION_BASE_URL}/user_handler/create'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=user_details) as response:
            return await response.json()


async def fetch_all_users_from_cloud_function():
    url = f'{CLOUD_FUNCTION_BASE_URL}/user_handler/read'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                return await response.json()  # Retornar o JSON da resposta
    except Exception as e:
        print(e)
        return {'error': str(e)}


def __main():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    user_details = {'address': 'Rua da Paz 4987', 'cpf': '14568598577', 'name': 'Ednaldo Pereira',
                    'phoneNumber': '+558597648593'}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(register_user_on_firebase(user_details))
    finally:
        loop.close()


if __name__ == '__main__':
    __main()

