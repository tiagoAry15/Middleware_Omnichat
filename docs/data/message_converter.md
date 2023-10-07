## message_converter.py

This module contains utilities and a class for converting and handling messages in various formats, primarily focusing 
on formatting user messages and dialogflow messages. It standardizes the format of incoming messages, which facilitates
further processing and provides uniformity in data management. 

Here is a detailed breakdown of its functionalities:

## message_converter.py

This module handles the conversion of messages from different sources like users and DialogFlow. It standardizes the format of incoming messages, which facilitates further processing and provides uniformity in data management.

### 📚 Imports:
- **json**: Used for parsing JSON data.
- **datetime**: Imported to format timestamps in messages.

### 🚀 Functions:
1. **get_user_message_example()**: 
    - Returns a dictionary containing an example of a user message with various attributes.
2. **get_dialogflow_message_example()**: 
    - Returns a dictionary containing an example of a Dialogflow message with various attributes.

### 🏗 Class: MessageConverterObject
This class contains methods to handle and convert messages dynamically.

#### Methods:
1. **__init__()**: 
    - Initializes the object with empty strings for `_from`, `phoneNumber`, and `sender` attributes.
2. **setMessageCoreDetails(sender, _from, phoneNumber)**: 
    - Sets core details of a message including sender, from, and phone number.
3. **dynamicConversion(message)**: 
    - Converts a message dynamically based on the object's current state, adding a timestamp to it.
4. **convertUserMessage(userMessage)**: 
    - A static method that converts a user message dictionary to a standardized format with a timestamp.
5. **convert_dialogflow_message(dialogflowMessage, userNumber)**: 
    - A static method that converts a Dialogflow message to a standardized format with a timestamp.

### 🎯 Main Function (__main__):
- Demonstrates the usage of `convertUserMessage` and `convert_dialogflow_message` methods by printing the converted messages to the console.

### 🔗 Usage:
This module can be imported wherever message conversion functionalities are needed, especially in routes where messages are being processed and emitted.

### 📝 Example:
```python
from data.message_converter import get_dialogflow_message_example, MessageConverterObject, get_user_message_example