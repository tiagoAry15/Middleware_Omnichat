## test_routes.py

This module defines a set of routes that are used for testing various functionalities of the API. It utilizes the Flask Blueprint to group these test-related routes. Here is a detailed breakdown of its functionalities:

### Imports:
- **json**: Used for parsing JSON data.
- **flask**: Imports `Blueprint`, `jsonify`, and `request` modules from Flask to create route blueprints and handle HTTP responses and requests respectively.
- **api_config**: Imports `fcm` and `socketio` from the `api_config.py` module to interact with Firebase services and manage Socket.IO integration respectively.
- **data.message_converter**: Imports various utilities to convert and get message examples.
- **socketEmissions.socket_emissor**: Imports `pulseEmit` function to emit messages to sockets.
- **utils.helper_utils**: Imports utility functions `__getUserByWhatsappNumber` and `sendWebhookCallback` for user retrieval and webhook callback handling respectively.

### Blueprint Initialization:
- **test_blueprint**: A blueprint instance is created to group all the test-related routes.

### Routes:
1. **/chatTest (GET)**: This route is used to test the chat functionality. It emits a series of user and Dialogflow messages to the socket, simulating a chat conversation.
2. **/staticReply (POST)**: This route is used to test the webhook callback functionality. It returns a static message as a response from the server.

### Usage:
This module is typically imported and registered in the main Flask application to add the test-related routes to the API, mainly for testing and debugging purposes.

### Example:
```python
from test_routes import test_blueprint
app.register_blueprint(test_blueprint, url_prefix='/test')
```

This snippet registers the test_blueprint to the Flask app with a URL prefix of '/test', making the routes defined in this module accessible under this URL prefix in the API for testing purposes.