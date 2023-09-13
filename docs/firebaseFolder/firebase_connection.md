## firebase_connection.py

This module facilitates the interaction with a Firebase Realtime Database through a singleton class named `FirebaseConnection`. It encapsulates various CRUD operations, including reading, writing, overwriting, and deleting data in the Firebase database. Here's a detailed breakdown of its functionalities:

### Class: FirebaseConnection

#### Methods:

- `__init__`: Initializes the FirebaseConnection as a singleton instance, setting up the connection to the Firebase database using the credentials and database URL from the environment variables.

- `changeDatabaseConnection(path: str) -> db.reference`: Changes the current active reference to another in the Firebase database. Takes a string path as an argument and returns a database reference.

- `readData(path: str = None) -> db.reference`: Reads and returns data from the specified path in the Firebase database. If no path is provided, it reads from the root. Returns a database reference.

- `writeData(path: str = None, data=None) -> bool`: Writes data to the specified path in the Firebase database. If no data is provided, it writes dummy data. Returns a boolean indicating the success of the operation.

- `overWriteData(path: str = None, data=None) -> bool`: Overwrites data at the specified path in the Firebase database. If no data is provided, it writes dummy data. Returns a boolean indicating the success of the operation.

- `deleteData(path: str = None, data=None) -> bool`: Deletes data at the specified path in the Firebase database. Requires the path and data to identify the unique ID for deletion. Returns a boolean indicating the success of the operation.

- `deleteAllData() -> bool`: Deletes all data at the root of the Firebase database. Returns a boolean indicating the success of the operation.

- `getUniqueIdByData(path: str = None, data=None) -> str`: Retrieves the unique key generated for the specified data at the given path in the Firebase database. Returns the unique key as a string.

### Usage:

To use this module, create an instance of the `FirebaseConnection` class and call the appropriate methods to interact with the Firebase database.

```python
fc = FirebaseConnection()
data = fc.readData("users")
```

### Note:
- This module uses the `firebase_admin` package to interact with the Firebase database.
- The singleton decorator ensures that only one instance of the FirebaseConnection class exists at any time.