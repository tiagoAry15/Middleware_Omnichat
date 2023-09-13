## intent_manager.py

This module is responsible for managing the intents and the flow of conversation in the chatbot. It integrates with Firebase for user management and handles the transition between different intents based on user input. It primarily consists of the `IntentManager` singleton class and a collection of utility functions and classes.

### Classes

#### `IntentNotFoundException`
A custom exception class that is raised when an intent is not found in the current set of intents.

#### `IntentManager`
A singleton class that manages the flow of conversation and handles the transition between different intents. It maintains a state that includes the current intent, user history, bot history, and other relevant information.

##### Attributes
- `fc`: An instance of `FirebaseConnection`.
- `fu`: An instance of `FirebaseUser`.
- `numberPot`: A list to store various numbers (not clear from the snippet).
- `whatsappNumber`: A string to store the user's WhatsApp number.
- `existingUser`: A boolean indicating whether the user exists in the database.
- `isUserChecked`: A boolean indicating whether the user's existence has been checked.
- `intents`: A list of available intents.
- `currentIntent`: The current active intent.
- `extractedParameters`: A dictionary to store parameters extracted during the conversation.
- `intentHistory`: A list to store the history of intents and their responses.
- `userHistory`: A list to store the history of user messages.
- `botHistory`: A list to store the history of bot responses.
- `signupDetails`: A dictionary to store the details of a user during the signup process.
- `count`: A counter to keep track of the number of interactions.
- `finished`: A boolean indicating whether the conversation has finished.

##### Methods
- `__getIntentByName`: A private method to get an intent by its name.
- `_analyzeBotResponse`: A method to analyze the bot's response and handle the transition between intents.
- `__handleIntentTransition`: A private method to handle the transition between intents.
- `isDefaultIntent`: A static method to check if the bot response is a default intent.
- `_handleBotAction`: A method to handle actions specified in the bot response.
- `chatBotLoop`: A method to simulate a chatbot loop using a console interface.
- `consoleLoop`: A method to implement a console-based chatbot loop.
- `twilioSingleStep`: A method to handle a single step in a Twilio-based chatbot loop.
- `existingWhatsapp`: A method to check if a WhatsApp number exists in the database.
- `registerWhatsapp`: A method to register a new WhatsApp number in the database.
- `__checkUserExistence`: A private method to check the existence of a user.
- `setWhatsappNumber`: A method to set the WhatsApp number and check the user's existence.
- `needsToSignUp`: A method to check if a user needs to sign up.
- `handleIncomingMessage`: A method to handle incoming messages in a Twilio-based chatbot loop.

### Functions
- `getIntentPot`: A function to get a list of initial intents for the signup process.
- `__main__`: A function to demonstrate the usage of the `IntentManager` class.

### Usage
To use this module, you can import it and create an instance of the `IntentManager` class. You can then use various methods of this class to manage the flow of conversation in your chatbot.

Example:
```python
from intent_manager import IntentManager

im = IntentManager()
message = "Hello"
response = im.handleIncomingMessage(message)
print(response)
```