# import random
#
# from gpt.greetingResponses import PizzaGreetingResponses
#
#
# class BotDialogue:
#     def __init__(self):
#         self.bot = PizzaGreetingResponses()
#
#     def start_dialogue(self):
#         active = True
#         while active:
#             self.printResponse(self.bot.sendGreetingResponse())
#             user_input = input("User: ")
#             if user_input == "stop":
#                 active = False
#
#     @staticmethod
#     def printResponse(response: str):
#         print("Bot:", response)
#
#
import openai


def __main():
    systemMsg = input("What type of chatbot would you like to create? ")
    messages = [{"role": "system", "content": systemMsg}]
    print("Say hello to your new assistant!")

    while input != "quit()":
        message = input()
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages)
        reply = response.choices[0].text
        messages.append({"role": "system", "content": reply})
        print("\n" + reply+"\n")


if __name__ == '__main__':
    __main()
