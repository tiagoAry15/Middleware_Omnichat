## dispatcher.py
This module is responsible for managing the dispatch of bot responses based on the user's input. It contains two main components: `BotOptions` and `BotDispatcher`.

### Classes

#### `BotOptions`
This class contains constants that represent different options and flows that the bot can undertake. These options include initiating a quiz, ordering a pizza, interacting with Twilio, registering a user, and rebooting a quiz. It also contains constants for quiz-related functionalities such as presenting questions, showing rankings, and listing alternatives.

Here are the attributes of the `BotOptions` class:
- `QUIZZ`: Represents the option to initiate a quiz.
- `PIZZA`: Represents the option to order a pizza.
- `TWILIO`: Represents the option to interact with Twilio.
- `REGISTER_USER`: Represents the option to register a user.
- `REBOOT_QUIZZ`: Represents the option to reboot a quiz.
- `QUESTION`: Represents the phase where a question is presented during a quiz.
- `RANKING`: Represents the phase where the ranking is shown during a quiz.
- `ALTERNATIVES`: A list of strings representing the possible alternatives during a quiz question.
- `QUIZZ_FLOW`: A list that aggregates various constants to represent the flow of a quiz session.

#### `BotDispatcher`
This class is responsible for handling the dispatch of bot responses based on the user's input. It maintains an attribute `intent` to keep track of the current intent of the bot, and a method `reply` to generate a response based on the user's message and the current intent.

Here are the attributes and methods of the `BotDispatcher` class:
- `QUIZZ_FLOW`: A constant representing a specific flow within the quiz functionality.
- `__init__`: A method to initialize a new instance of the `BotDispatcher` class, setting the initial intent to `Replies.WELCOME`.
- `reply`: A method that takes a user message as input and returns a formatted response based on the current intent and the user's message.
- `format`: A method (not shown in the snippet) that presumably formats a reply before returning it (needs to be implemented).

### Functions
- `__main__`: A function to demonstrate the usage of the `BotDispatcher` class by creating an instance and printing a reply to a sample message.

### Usage
To use this module, you can import it and create an instance of the `BotDispatcher` class, then use the `reply` method to get responses based on user messages. You can also utilize the `BotOptions` class to reference various bot options and flows in your implementation.

Example:
```python
from dispatcher import BotDispatcher

dispatcher = BotDispatcher()
message = "Hello"
response = dispatcher.reply(message)
print(response)
