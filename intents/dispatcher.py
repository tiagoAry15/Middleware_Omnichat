from intents.replies import Replies


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

    @staticmethod
    def format(reply_pair: dict):
        text = reply_pair.get("main")
        media = reply_pair.get("media")
        choices = [value for key, value in reply_pair.items() if key.isdigit()]
        menu = '\n'.join([f"{key}-{value}" for key, value in enumerate(choices, start=1)])
        sentence = f"{text}\n{menu}"
        r = {"body": sentence}
        if media is not None:
            r["media"] = media
        return r

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
