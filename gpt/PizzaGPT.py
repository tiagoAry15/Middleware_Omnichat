import os

import openai
from dotenv import load_dotenv
import json

from gpt import phraseEnum
from gpt.phraseEnum import PhraseEnum
from gpt.timeDecorator import timingDecorator
from intentManipulation.intentManagerTiago import IntentManager


def readTxtAndConvertToString(filepath: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except IOError:
        return "Error: Could not read the file."


def getPizzaGPTPrompt(prompt: str):
    baseString = readTxtAndConvertToString('./chatGPTPrompt.txt')
    return f'{baseString} "{prompt}"?'


@timingDecorator
def getResponseDefaultGPT(prompt: str):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=100,
    )
    choice = completion.choices[0]
    return choice.text


def parseGPTAnswer(gptAnswer: str):
    cleanedAnswer = gptAnswer.replace("\n", "")
    return json.loads(cleanedAnswer)


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

    def getResponseChatGPT(self, prompt: str):
        try:
            self.messages.append({"role": "user", "content": prompt})
            self.completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
        except openai.error.RateLimitError as e:
            return "Estamos com muita mensagens no momento, repita a mensagem dentro de instantes"

        gpt_response = json.loads(self.completion.choices[-1]["message"]["content"])
        return IntentManager.process_intent(gpt_response)

    def readJsonAndConvertToString(self, filepath: str):
        with open(filepath, "r") as file:
            json_content = json.load(file)
            self.intents_dictionary = json.dumps(json_content)


def gptPipeline(prompt: str = "Vou querer duas pizzas calabresas, e uma pizza meio pepperoni meio portuguesa"):
    load_dotenv()
    fullPrompt = getPizzaGPTPrompt(prompt)
    output = getResponseDefaultGPT(fullPrompt)
    return parseGPTAnswer(output)


def __main():
    return gptPipeline()


if __name__ == '__main__':
    __main()
