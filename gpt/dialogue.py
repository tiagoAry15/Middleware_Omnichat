import random

from gpt.botDialogue import PizzaBotDialogue


class BotDialogue:
    def __init__(self):
        self.bot = PizzaBotDialogue()

    def start_dialogue(self):
        active = True
        while active:
            self.printResponse(self.bot.sendGreetingResponse())
            user_input = input("User: ")
            if user_input == "stop":
                active = False

    @staticmethod
    def printResponse(response: str):
        print("Bot:", response)


def __main():
    bot = BotDialogue()
    bot.start_dialogue()


if __name__ == '__main__':
    __main()
