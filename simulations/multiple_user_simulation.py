import uuid
from typing import List
import asyncio
from ipAddressSessions.signupBot_session_manager import SignupBotFactory
from signupBot.intent_manager import SignupBot


async def single_signup_bot_user_simulation(user_id: str, message_pool: list):
    manager = SignupBotFactory()
    ds: SignupBot = manager.get_session(user_id)

    response_dict = {}
    for message in message_pool:
        response = await ds.twilioSingleStep(userMessage=message)  # await the coroutine
        response_dict[message] = response
    return response_dict


async def run_simulation(user1_messages: List[str], user2_messages: List[str], simulation_function):
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())

    # Using asyncio.gather to run both simulations concurrently
    user1_results, user2_results = await asyncio.gather(
        simulation_function(user1_id, user1_messages),
        simulation_function(user2_id, user2_messages)
    )

    print("User 1 Results:", user1_results)
    print("User 2 Results:", user2_results)


async def __main():
    user_1_messages = ["Oii", "Clark Kent", "Avenida da Paz 2845"]
    user_2_messages = ["Oii", "Bruce Wayne", "Rua das Flores 4874"]
    await run_simulation(user_1_messages, user_2_messages, single_signup_bot_user_simulation)  # await the function call


if __name__ == "__main__":
    asyncio.run(__main())  # Use asyncio.run for Python 3.7+
