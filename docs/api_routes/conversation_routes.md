## conversation_routes.py

This module defines the routes and respective views for handling conversation-related operations in the API. It utilizes the Flask Blueprint to group conversation-related routes. Here is a detailed breakdown of its functionalities:

### 🛠 Key Components:

1. **📃 Conversation Blueprint**
    - Initialization of the blueprint specific to conversation-related routes.

2. **📁 Get All Conversations**
    - Endpoint: `/get_all_conversations`
    - Method: `GET`
    - Description: Retrieves all the conversations from the firebase database and returns them in a JSON format.

3. **📞 Get Conversation by Whatsapp Number**
    - Endpoint: `/get_conversation_by_whatsapp_number/<whatsappNumber>`
    - Method: `GET`
    - Description: Fetches a specific conversation tied to a given Whatsapp number.

4. **📝 Create a New Conversation**
    - Endpoint: `/create_conversation`
    - Method: `POST`
    - Description: Processes incoming data to create a new conversation.

5. **🔄 Update Conversation**
    - Endpoint: `/update_conversation`
    - Method: `PUT`
    - Description: Updates a specific conversation based on the provided data.

6. **➕ Update Conversation by Adding Unread Messages**
    - Endpoint: `/update_conversation_adding_unread_messages`
    - Method: `PUT`
    - Description: Modifies a conversation by appending unread messages.

7. **❌ Delete Conversation**
    - Endpoint: `/delete_conversation`
    - Method: `DELETE`
    - Description: Erases a specific conversation based on the incoming data.

8. **💬 Push New Message by Whatsapp Number**
    - Endpoint: `/push_new_message_by_whatsapp_number/`
    - Method: `POST`
    - Description: Adds a new message to an existing conversation identified by the provided Whatsapp number.

9. **📤 Send Message to User**
    - Endpoint: `/send_message_to_user/<user_number>`
    - Method: `POST`
    - Description: Utilizes the Twilio API to send a message to a given user, and also appends this message to the conversation.

### Imports:
- **json**: Used for parsing JSON data.
- **flask**: Imports `Blueprint`, `jsonify`, and `request` modules from Flask to create route blueprints and handle HTTP responses and requests respectively.
- **api_config**: Imports `fcm`, `twilioClient`, and `twilio_phone_number` from the `api_config.py` module to interact with Firebase and Twilio services.
- **utils.helper_utils**: Imports the `__getUserByWhatsappNumber` utility function to get user details using their WhatsApp number.

### Blueprint Initialization:
- **conversation_blueprint**: A blueprint instance is created to group all the conversation-related routes.

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