from intentManipulation.replies import Replies


class BotOptions:
    QUIZZ = "1"
    PIZZA = "2"
    TWILIO = "3"
    REGISTER_USER = "7"
    REBOOT_QUIZZ = "8"

    QUESTION = "P"
    RANKING = "r"
    ALTERNATIVES = ["a", "b", "c", "d"]
    QUIZZ_FLOW = [QUIZZ, REGISTER_USER, REBOOT_QUIZZ, QUESTION, RANKING] + ALTERNATIVES


class BotDispatcher:
    QUIZZ_FLOW = 7777

    def __init__(self):
        self.intent = Replies.WELCOME

    def reply(self, userMessage):
        message = userMessage.lower()
        if self.intent == Replies.WELCOME:
            return self.format(Replies.WELCOME)


def __main():
    dispatcher = BotDispatcher()
    message = "Oii"
    print(dispatcher.reply(message))


if __name__ == "__main__":
    __main()
