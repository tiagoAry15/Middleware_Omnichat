import os
import asyncio
from api_config.object_factory import ucm


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
