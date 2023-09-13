## firebase_user.py

This module contains the `FirebaseUser` class which extends the `FirebaseWrapper` class, and is responsible for managing user data in a Firebase Realtime Database. It includes methods to create, read, update, and delete user data, as well as utility methods to handle user-specific operations.

### Class: FirebaseUser

#### Methods:

- `__init__(self, inputFirebaseConnection: FirebaseConnection)`: Initializes a new instance of the FirebaseUser class, accepting a FirebaseConnection object as a parameter.

- `updateConnection()`: Updates the database connection to point to the "users" node in the Firebase database.

- `getAllUsers()`: Retrieves all users from the Firebase database.

- `getUniqueIdByPhoneNumber(phoneNumber: str) -> str or None`: Retrieves the unique ID of a user by their phone number. Returns the unique ID as a string or None if not found.

- `existingUser(inputUserData: dict) -> bool`: Checks if a user exists in the database. Takes a dictionary containing user data as a parameter and returns a boolean indicating the existence of the user.

- `createUser(userData: dict) -> bool`: Creates a new user in the database. Takes a dictionary containing user data as a parameter and returns a boolean indicating the success of the operation.

- `updateUser(userData: dict) -> bool`: Updates an existing user in the database. Takes a dictionary containing user data as a parameter and returns a boolean indicating the success of the operation.

- `deleteUser(userData: dict) -> bool`: Deletes a user from the database. Takes a dictionary containing user data as a parameter and returns a boolean indicating the success of the operation.

### Utility Functions:

- `__createDummyUsers()`: Creates dummy users in the Firebase database for testing purposes. This function is called in the `__main__` function to populate the database with dummy data.

### Usage:

To use this module, create an instance of the `FirebaseUser` class and call the appropriate methods to interact with the Firebase database.

```python
fc = FirebaseConnection()
fu = FirebaseUser(fc)
fu.getAllUsers()
```

### Notes:
- This module uses the `singleton` and `update_connection_decorator` decorators to ensure that only one instance of the `FirebaseUser` class exists at any time and to update the database connection respectively.