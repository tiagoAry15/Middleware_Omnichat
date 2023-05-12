import random


class BotDialogue:
    def __init__(self):
        self.botResponses = [
            "I'm sorry, I didn't understand that.",
            "Could you please rephrase your statement?",
            "Interesting! Tell me more.",
            "That's a good point.",
            "I'm here to help. What can I assist you with?"
        ]

    def start_dialogue(self):
        active = True
        while active:
            user_input = input("User: ")
            if user_input != "stop":
                self.bot_response()
            else:
                active = False

    def bot_response(self):
        random_response = random.choice(self.botResponses)
        print("Bot:", random_response)


def __main():
    bot = BotDialogue()
    bot.start_dialogue()


if __name__ == '__main__':
    __main()
