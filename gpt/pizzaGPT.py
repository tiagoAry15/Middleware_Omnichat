import os

import openai
from dotenv import load_dotenv

from timeDecorator import timingDecorator


class pizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

    @timingDecorator
    def get_response_gpt(self, prompt: str):
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
        )
        choice = completion.choices[0]
        return choice.text

    @timingDecorator
    def get_response_chat_gpt(self, prompt: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0]["message"]["content"]


def __main():
    p = pizzaGPT()
    response = p.get_response_chat_gpt("What is the difference between Celsius and Fahrenheit?")
    print(response)
    return response


if __name__ == '__main__':
    __main()
