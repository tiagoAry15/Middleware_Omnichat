## user_routes.py

This module defines the routes and respective views for handling user-related operations in the API. It utilizes the Flask Blueprint to group user-related routes. Here is a detailed breakdown of its functionalities:

### Imports:
- **json**: Used for parsing JSON data.
- **flask**: Imports `Blueprint`, `jsonify`, and `request` modules from Flask to create route blueprints and handle HTTP responses and requests respectively.
- **api_config**: Imports `fcm` from the `api_config.py` module to interact with Firebase services.
- **utils.helper_utils**: Imports the `__getUserByWhatsappNumber` utility function to get user details using their WhatsApp number.

### Blueprint Initialization:
- **user_blueprint**: A blueprint instance is created to group all the user-related routes.

### Routes:
1. **/get_all_users (GET)**: Retrieves all users from the Firebase database.
2. **/get_user_by_whatsapp_number (GET)**: Retrieves a specific user using the WhatsApp number from the Firebase database.
3. **/create_user (POST)**: Creates a new user in the Firebase database with the provided data.
4. **/update_user (PUT)**: Updates an existing user in the Firebase database with the provided data.
5. **/delete_user (DELETE)**: Deletes a user from the Firebase database using the provided data.

### Error Handling:
- The routes have error handling in place to return appropriate error messages and status codes in case of any issues.

### Usage:
This module is typically imported and registered in the main Flask application to add the user-related routes to the API.

### Example:
```python
from user_routes import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
```
This snippet registers the user_blueprint to the Flask app with a URL prefix of '/users', making the routes defined in this module accessible under this URL prefix in the API.