## conversation_routes.py

This module defines the routes and respective views for handling conversation-related operations in the API. It utilizes the Flask Blueprint to group conversation-related routes. Here is a detailed breakdown of its functionalities:

### Imports:
- **json**: Used for parsing JSON data.
- **flask**: Imports `Blueprint`, `jsonify`, and `request` modules from Flask to create route blueprints and handle HTTP responses and requests respectively.
- **api_config**: Imports `fcm`, `twilioClient`, and `twilio_phone_number` from the `api_config.py` module to interact with Firebase and Twilio services.
- **utils.helper_utils**: Imports the `__getUserByWhatsappNumber` utility function to get user details using their WhatsApp number.

### Blueprint Initialization:
- **conversation_blueprint**: A blueprint instance is created to group all the conversation-related routes.

### Routes:
1. **/get_all_conversations (GET)**: Retrieves all conversations from the Firebase database.
2. **/get_conversation_by_whatsapp_number/<whatsappNumber> (GET)**: Retrieves a specific conversation using the WhatsApp number.
3. **/create_conversation (POST)**: Creates a new conversation in the Firebase database with the provided data.
4. **/update_conversation (PUT)**: Updates an existing conversation in the Firebase database with the provided data.
5. **/update_conversation_adding_unread_messages (PUT)**: Updates a conversation by adding unread messages to it in the Firebase database.
6. **/delete_conversation (DELETE)**: Deletes a conversation from the Firebase database using the provided data.
7. **/push_new_message_by_whatsapp_number/ (POST)**: Adds a new message to a conversation identified by the WhatsApp number.
8. **/send_message_to_user/<user_number> (POST)**: Sends a message to a user using Twilio service and adds the message to the conversation in the Firebase database.

### Error Handling:
- The routes have error handling in place to return appropriate error messages and status codes in case of any issues.

### Usage:
This module is typically imported and registered in the main Flask application to add the conversation-related routes to the API.

### Example:
```python
from conversation_routes import conversation_blueprint
app.register_blueprint(conversation_blueprint, url_prefix='/conversations')
```

This snippet registers the conversation_blueprint to the Flask app with a URL prefix of '/conversations', making the routes defined in this module accessible under this URL prefix in the API.