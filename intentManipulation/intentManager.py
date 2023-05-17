from typing import List

from colorama import Fore, Style

from intentManipulation.intentTypes.intentFallback import FallbackIntent
from intentManipulation.intentTypes.intentMultipleChoice import MultipleChoiceIntent
from intentManipulation.intentTypes.replies import Replies, Types


def getIntentPot():
    return [MultipleChoiceIntent(Replies.WELCOME), FallbackIntent(Replies.MENU)]


class IntentManager:
    def __init__(self, intents: List):
        self.intents = intents
        self.currentIntent = intents[0]
        self.intentHistory = []
        self.botResponseHistory = []

    def __getIntentByName(self, inputIntentName: str):  # sourcery skip: use-next
        for intent in self.intents:
            currentName = intent.reply["intentName"].lower()
            if currentName == inputIntentName.lower():
                return intent
        return None

    def _analyzeBotResponse(self, botResponse: dict):
        botAnswer = ""
        if self.isDefaultIntent(botResponse):
            botAnswer = botResponse["body"]
        else:
            botAnswer = self.__handleIntentTransition(botResponse)
        self.intentHistory.append(self.currentIntent)
        self.botResponseHistory.append(botAnswer)
        print(f"{Fore.YELLOW}Bot:{Style.RESET_ALL} {botAnswer}")

    def __handleIntentTransition(self, botResponse: dict):
        nextIntentName = botResponse["changeIntent"]
        nextIntent = self.__getIntentByName(nextIntentName)
        self.intentHistory.append(nextIntent)
        nextIntentAnswer = nextIntent.sendFirstMessage()["body"]
        previousBotAnswer = self.botResponseHistory[-1]
        return f"{nextIntentAnswer}\n\n{previousBotAnswer}"

    @staticmethod
    def isDefaultIntent(botResponse):
        return list(botResponse.keys()) == ["body"]

    def handleIntentChanges(self, botResponse):
        if "changeIntent" not in botResponse:
            return botResponse["body"]
        nextIntent = botResponse["changeIntent"]
        newIntentObject = self.__getIntentByName(nextIntent)
        isNextIntentFallback = newIntentObject.intentType == Types.FALLBACK
        if isNextIntentFallback:
            return newIntentObject.sendFirstMessage()["body"], self.botResponsesHistory[-1]
        if newIntentObject is None:
            raise ValueError(f"Intent {nextIntent} not found.")
        self.currentIntent = newIntentObject
        return self.currentIntent.sendFirstMessage()["body"]

    def chatBotLoop(self):
        """This function simulates a chatbot loop."""
        while True:
            userMessage = input(f"{Fore.RED}User: {Style.RESET_ALL}")
            botResponse = self.currentIntent.parseIncomingMessage(userMessage)
            self._analyzeBotResponse(botResponse)


"""The approach presented in the code can work for handling fallback intents. However, depending on the complexity 
of your chatbot and the desired behavior for fallbacks, there may be alternative approaches that offer more flexibility
or better organization. Here are a few suggestions:
  
    1. Fallback as a separate Intent class: Instead of handling fallbacks within the IntentManager class, you could 
create a separate FallbackIntent class inheriting from the Intent class. This can help keep the code  modular and make
it easier to add or modify fallback behavior in the future.
  
    2. Implement a stack-based approach: Instead of relying on the botResponsesHistory list, you could use a stack to 
manage the conversation flow. Each time a new intent is triggered, you push it onto the stack. When a fallback occurs,
you pop the stack to return to the previous intent. This can handle nested fallbacks more effectively and provide 
a clearer mechanism for managing intent transitions.
   
    3. Use a state machine design: Consider implementing a state machine to model the chatbot's behavior. 
Each intent can represent a state, and the transitions between intents can be defined explicitly. This approach provides
a more structured way to handle fallbacks and allows for more complex conversation flows.

    4. Implement a natural language understanding (NLU) system: For more sophisticated chatbots, consider incorporating
a natural language understanding system that can analyze user input and determine the intent automatically. This can
handle fallbacks and intent recognition more effectively, enabling more dynamic conversation handling.
"""


def __main():
    listOfIntents = getIntentPot()
    im = IntentManager(listOfIntents)
    im.chatBotLoop()
    return


if __name__ == "__main__":
    __main()
