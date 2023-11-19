## api_config.py

This module encapsulates the core functionalities of webhooks, order processing, and route handling for the main API. 
It's seamlessly integrated with key components like DialogFlow, Twilio, and Instagram, paving the way for dynamic user 
interactions and data flows

### 🛠 Key Components:

1. **📦 API Blueprints**
    - Registration of various API blueprints related to conversations, users, and testing.

2. **📞 Twilio Sandbox Endpoint**
    - Handles incoming POST requests from the Twilio Sandbox, facilitating real-time interactions with the user and response processing via DialogFlow.

3. **🔮 DialogFlow Webhook Endpoint**
    - Serves as a callback for DialogFlow, processing user intents, and generating appropriate responses. Notably, it includes specific handlers for different ordering scenarios like pizza and drinks.

4. **📬 Twilio Webhook Endpoints**
    - The module listens to both pre-event and post-event webhooks from Twilio, enabling the system to intercept and react to messages respectively.

5. **📸 Instagram Endpoint**
    - Designed to communicate with the Instagram API. It can accept subscription challenges and process incoming messages from Instagram, converting them to a standardized format and handling them accordingly.

6. **🚀 Execution & Deployment**
    - The component's runtime logic, specifying the host and port details for the Flask app, and initializing the Socket.io events.

### Imports and Initializations:
- **os, dotenv**: These modules are used to interact with the environment variables which store sensitive information like Twilio credentials.
- **Flask, Flask_CORS, FlaskSocketIO**: These are Flask modules used to create the Flask application, handle Cross-Origin Resource Sharing (CORS), and manage Socket.IO integration respectively.
- **Twilio Client**: This is initialized to interact with the Twilio API using the credentials stored in the environment variables.
- **FirebaseConnection, FirebaseUser, FirebaseConversation**: These are classes imported to handle various Firebase operations.
- **DialogFlowSession**: This is imported to manage the Dialogflow session.
- **MessageConverter**: This is imported to handle message conversions.

### Flask Application Setup:
- The Flask application instance (`app`) is created and CORS is configured to allow requests from specified origins.
- Socket.IO is set up to allow communication between the client and the server through sockets.
- A route (`'/'`) is defined which returns a "Hello, World!" message when accessed.

### Main Function (`__main__`):
- This function is responsible for starting the Flask application with the configured settings. It is called when the script is run directly.

### Global Variables:
- Several global variables are initialized to hold instances of various classes and configurations, which can be used throughout the application. These include instances for DialogFlow session, Firebase connection, user and conversation handling, message conversion, and Twilio client.

### Usage:
This module is generally imported in other modules to access the initialized instances and the Flask application settings. It acts as a central configuration file where all the necessary components for the API are set up and made ready for use.

### Example:

```python
from api_config.api_setup import socketio
from api_config.core_factory import core_app
from api_config.object_factory import menuHandler
```

This line of code imports the Flask app instance, the Socket.IO instance, and the DialogFlow session instance from the api_config.py module, ready to be used in other parts of the application.