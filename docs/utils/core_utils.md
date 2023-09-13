## _core_utils.py_

This module is responsible for handling and processing user messages, particularly those coming from the Twilio API and interacting with the DialogFlow API for message responses. Here are the functionalities provided by this module:

### Functions

- **processUserMessage(data: dict)**: This function processes the user message data, transforms it into a structured format suitable for Firebase, and appends the message to the respective WhatsApp number conversation in Firebase Cloud Messaging (FCM).

- **__transformTwilioDataIntoStructuredFirebaseData(data: dict) -> dict**: This private function transforms the raw data received from Twilio into a structured format, including extracting the current time, phone number, and other relevant details.

- **__checkUserRegistration(phoneNumber: str)**: This private function checks if a user, identified by their phone number, is registered in the system.

- **__handleNewUser(phoneNumber: str, receivedMessage: str)**: This private function handles the registration and initial message processing for new users. It logs the necessary information and interacts with the DialogFlow API to generate a response.

- **__handleExistingUser(phoneNumber: str, receivedMessage: str)**: This private function handles message processing for existing users, interacting with the DialogFlow API to generate a response.

- **processDialogFlowMessage(messageData: dict)**: This function processes messages through DialogFlow, determining whether the user is new or existing and handling the message accordingly.

- **processTwilioSandboxIncomingMessage(data: dict)**: This function processes incoming messages from the Twilio sandbox, handling both new and existing users and emitting the processed message data through a socket.

- **__main()**: A testing function that demonstrates the usage of various functions within the module with a predefined data dictionary.

### Usage

This module is primarily used to process incoming messages from users, interacting with both the Twilio and DialogFlow APIs to generate appropriate responses and maintain conversation histories in Firebase.

### Examples

The `__main__` function within the module provides a demonstration of how to use the functions to process a sample message data dictionary.

```python
d1 = {
    "SmsMessageSid": "SMc7f2b5f0c0a4b0b0a1a0a1a0a1a0a1a0",
    "NumMedia": "0",
    "SmsSid": "SMc7f2b5f0c0a4b0b0a1a0a1a0a1a0a1a0",
    "SmsStatus": "received",
    "Body": "oi",
    "To": "whatsapp:+14155238886",
    "NumSegments": "1",
    "MessageSid": "SMc7f2b5f0c0a4b0b0a1a0a1a0a1a0a1a0",
    "AccountSid": "AC034f7d97b8d5bc62dfa91b519ac43b0f",
    "From": "whatsapp:+558599663533",
    "ApiVersion": "2010-04-01"
}
```