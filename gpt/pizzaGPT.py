import os

import openai
from dotenv import load_dotenv
import json
from timeDecorator import timingDecorator


class pizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.intents_dictionary = {}

    @timingDecorator
    def get_response_gpt(self, prompt: str):
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.get_response(prompt),
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

    def read_json_and_convert_to_string(self, filepath: str):
        with open(filepath, "r") as file:
            json_content = json.load(file)
            self.intents_dictionary = json.dumps(json_content)

    def get_response(self, prompt: str):
        return "Dada a seguinte mensagem: "  + prompt + ", qual é a intenção do usuário com base nos exemplos de intenções no arquivo JSON abaixo?\n\n" + self.intents_dictionary


def __main():
    p = pizzaGPT()
    p.read_json_and_convert_to_string('./chatGPT_training.json')

    response = p.get_response_gpt("Boa noite")
    print(response)
    response = p.get_response_gpt("quero ver as opções")
    print(response)
    response = p.get_response_gpt("quero fazer um pedido")
    print(response)
    response = p.get_response_gpt("quero 3 pizzas")
    print(response)
    return response


if __name__ == '__main__':
    __main()
