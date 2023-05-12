import os

import openai
from dotenv import load_dotenv

from timeDecorator import timingDecorator


class pizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

    @timingDecorator
    def get_response(self, prompt: str):
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
        )
        choice = completion.choices[0]
        return choice.text


def __main():
    p = pizzaGPT()
    response = p.get_response("What is the difference between Celsius and Fahrenheit?")
    print(response)
    return response


if __name__ == '__main__':
    __main()
