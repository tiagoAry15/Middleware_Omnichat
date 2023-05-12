import os

import openai
from dotenv import load_dotenv


class pizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
