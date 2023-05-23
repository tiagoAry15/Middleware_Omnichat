import os

import openai
from dotenv import load_dotenv
import json

from gpt import phraseEnum
from gpt.phraseEnum import PhraseEnum
from intentManipulation.intentManagerTiago import IntentManager


def get_response_default_gpt(prompt: str):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=100,
    )
    choice = completion.choices[0]
    return choice.text


class PizzaGPT:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.intents_list = ['welcome', 'order_pizzas', 'order_drinks', 'confirm_order']
        self.init_phrase = PhraseEnum.FRASE_INICIAL.value
        self.messages = [{"role": "user", "content": self.init_phrase}]
        self.intents_dictionary = {}
        self.completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

    def get_response_chat_gpt(self, prompt: str):
        try:
            self.messages.append({"role": "user", "content": prompt})
            self.completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
        except openai.error.RateLimitError as e:
            return "Estamos com muita mensagens no momento, repita a mensagem dentro de instantes"

        gpt_response = json.loads(self.completion.choices[-1]["message"]["content"])
        refactored_response = IntentManager.process_intent(gpt_response)
        return refactored_response

    def read_json_and_convert_to_string(self, filepath: str):
        with open(filepath, "r") as file:
            json_content = json.load(file)
            self.intents_dictionary = json.dumps(json_content)



def __main():
    p = PizzaGPT()
    p.read_json_and_convert_to_string('./chatGPT_training.json')

    response = get_response_default_gpt("Boa noite")
    print(response)
    response = get_response_default_gpt("quero ver as opções")
    print(response)
    response = get_response_default_gpt("quero fazer um pedido")
    print(response)
    response = get_response_default_gpt("quero 3 pizzas")
    print(response)
    return response


if __name__ == '__main__':
    __main()
