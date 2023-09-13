## firebase_conversation.py

This module contains the `FirebaseConversation` class which extends the `FirebaseWrapper` class, and is responsible for managing conversations in a Firebase Realtime Database. It includes methods to create, read, update, and delete conversation data, as well as utility methods to handle conversation-specific operations.

### Class: FirebaseConversation

#### Methods:

- `__init__(self, inputFirebaseConnection: FirebaseConnection)`: Initializes a new instance of the FirebaseConversation class, accepting a FirebaseConnection object as a parameter.

- `updateConnection()`: Updates the database connection to point to the "conversations" node in the Firebase database.

- `getAllConversations()`: Retrieves all conversations from the Firebase database.

- `getConversationByWhatsappNumber(whatsappNumber: str) -> dict or None`: Retrieves a conversation by the WhatsApp number. Returns a dictionary containing the conversation data or None if not found.

- `getUniqueIdByWhatsappNumber(whatsappNumber: str) -> str or None`: Retrieves the unique ID of a conversation by the WhatsApp number. Returns the unique ID as a string or None if not found.

- `appendMessageToWhatsappNumber(messageData: dict, whatsappNumber: str)`: Appends a message to a conversation identified by the WhatsApp number. Takes a dictionary containing message data and a string representing the WhatsApp number as parameters.

- `retrieveAllMessagesByWhatsappNumber(whatsappNumber: str) -> List[dict] or None`: Retrieves all messages from a conversation identified by the WhatsApp number. Returns a list of dictionaries containing message data or None if not found.

- `createFirstDummyConversationByWhatsappNumber(msgDict: dict)`: Creates a dummy conversation using the data provided in the msgDict parameter.

- `existingConversation(inputConversationData: dict) -> bool`: Checks if a conversation exists in the database. Takes a dictionary containing conversation data as a parameter and returns a boolean indicating the existence of the conversation.

- `createConversation(conversationData: dict) -> bool`: Creates a new conversation in the database. Takes a dictionary containing conversation data as a parameter and returns a boolean indicating the success of the operation.

- `updateConversation(conversationData: dict) -> bool`: Updates an existing conversation in the database. Takes a dictionary containing conversation data as a parameter and returns a boolean indicating the success of the operation.

- `updateConversationAddingUnreadMessages(messageData: dict) -> bool`: Updates the unread messages count in a conversation. Takes a dictionary containing message data as a parameter and returns a boolean indicating the success of the operation.

- `deleteConversation(conversationData: dict) -> bool`: Deletes a conversation from the database. Takes a dictionary containing conversation data as a parameter and returns a boolean indicating the success of the operation.

- `deleteAllConversations()`: Deletes all conversations from the database.

### Utility Functions:

- `getDummyConversationDicts(username: str = "John", phoneNumber: str = "+558599171902", _from: str = "whatsapp")`: Generates dummy conversation data. Takes username, phone number, and platform as parameters and returns a dictionary containing dummy conversation data.

- `checkNewUser(whatsappNumber: str, numberPot: List[str], conversationInstance: FirebaseConversation, msgDict: dict) -> bool`: Checks if a user is new and creates a dummy conversation for them if true. Takes WhatsApp number, a list of phone numbers, a FirebaseConversation instance, and a message dictionary as parameters. Returns a boolean indicating whether the user is new.

### Usage:

To use this module, create an instance of the `FirebaseConversation` class and call the appropriate methods to interact with the Firebase database.

```python
fc = FirebaseConnection()
fcm = FirebaseConversation(fc)
fcm.getAllConversations()
```

### Note:

- This module uses the `firebase_admin` package to interact with the Firebase database.
- This module uses the datetime, random, and uuid packages to facilitate various operations.
- The singleton decorator ensures that only one instance of the FirebaseConversation class exists at any time.