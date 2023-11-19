import os
import asyncio

from api_config.core_factory import core_app
from cache.whatsapp_user_cache import UserCacheManager

ucm = UserCacheManager(core_app)


async def update_user_cache():
    await ucm.refresh_cache()


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(update_user_cache())
    finally:
        loop.close()
