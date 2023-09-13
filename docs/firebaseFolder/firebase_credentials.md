## firebase_credentials.py

This module is responsible for managing the Firebase credentials in the application. It facilitates the retrieval of Firebase credentials from environment variables and prepares them in a format suitable for authentication with Firebase services. Here are the primary responsibilities of this module:

- Loading environment variables using `dotenv`.
- Formatting the private key correctly to be used in Firebase authentication.
- Constructing a dictionary with Firebase credentials gathered from environment variables.

### Functions

#### `getFirebaseCredentials()`
This function retrieves Firebase credentials from environment variables, formats the private key correctly, and returns a Firebase credentials object which can be used to authenticate with Firebase services.

#### `__main__()`
A main function that calls `getFirebaseCredentials` function and can be used for testing or initializing the credentials during script execution.

### Usage

To use this module, import it in your script and call `getFirebaseCredentials` to get the Firebase credentials object. You can then use this object to initialize your Firebase application.

```python
from firebase_credentials import getFirebaseCredentials

firebase_creds = getFirebaseCredentials()
# Use firebase_creds to initialize Firebase application
```

### Note
Ensure that the necessary environment variables are set in your .env file before using this module to avoid KeyError. The required environment variables are:

- FIREBASE_SDK_TYPE
- FIREBASE_SDK_PROJECT_ID
- FIREBASE_SDK_PRIVATE_KEY_ID
- FIREBASE_SDK_PRIVATE_KEY
- FIREBASE_SDK_CLIENT_EMAIL
- FIREBASE_SDK_CLIENT_ID
- FIREBASE_SDK_AUTH_URI
- FIREBASE_SDK_TOKEN_URI
- FIREBASE_SDK_AUTH_PROVIDER_X509_CERT_URL
- FIREBASE_SDK_CLIENT_X509_CERT_URL