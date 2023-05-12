import os

import openai
from dotenv import load_dotenv


class pizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def get_response(self, prompt: str):
        return openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}])


def __main():
    p = pizzaGPT()
    response = p.get_response("What is the difference between Celsius and Fahrenheit?")
    print(response)
    return response


if __name__ == '__main__':
    __main()
