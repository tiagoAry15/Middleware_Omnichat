## _helper_utils.py_

This module contains utility functions that assist in various tasks such as preparing responses for DialogFlow, handling webhook callbacks, and interacting with the Twilio API. Here are the functionalities provided by this module:

### Functions

- **__prepareOutputResponse(myResult) -> Response**: A private function that prepares a JSON response from the given result, setting the appropriate content type before returning it.

- **sendWebhookCallback(botMessage: str, nextContext: List = None) -> Response**: This function prepares a response for a webhook callback with the specified bot message and optional context, returning a JSON response.

- **changeDialogflowIntent(newIntent: str = None, parameters: dict = None) -> Response**: This function allows for the changing of the DialogFlow intent, accepting new intent and parameters as arguments and returning a prepared JSON response.

- **changeDialogflowContext(newContext: str = None, parameters: dict = None) -> Response**: This function facilitates the modification of the DialogFlow context, taking new context and parameters as arguments and returning a prepared JSON response.

- **getDialogFlowAuth()**: This function retrieves authentication details for DialogFlow from environment variables and prints the base64 encoded authentication string.

- **extractDictFromBytesRequest() -> dict**: This function extracts a dictionary from a byte request, useful for parsing incoming requests.

- **getJsonCredentialsData() -> dict**: This function retrieves JSON credentials data from a specified file path.

- **__getAllUsersMappedByPhone() -> dict**: A private function that retrieves all users from Firebase and maps them by phone number.

- **__getUserByWhatsappNumber(whatsappNumber: str) -> dict or None**: A private function that retrieves user details by their WhatsApp number from the Firebase database.

- **__addBotMessageToFirebase(phoneNumber, userMessageJSON)**: A private function that adds a bot message to Firebase, taking the phone number and message JSON as arguments.

- **sendTwilioResponse(body: str, media: str = None) -> str**: This function prepares a response for the Twilio API, accepting a message body and optional media URL as arguments, and returning the formatted response string.

- **__main()**: A placeholder function for potential future use or testing.

### Usage

This module is used to facilitate various functionalities in the application, including preparing responses for DialogFlow, handling webhook callbacks, and interacting with the Twilio API.

