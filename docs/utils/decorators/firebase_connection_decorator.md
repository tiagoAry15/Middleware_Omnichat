## _firebase_connection_decorator.py_
This module contains a decorator that ensures the connection to Firebase is updated before the execution of the decorated function. Here are the functionalities it provides:

- `update_connection_decorator(func)`: A decorator that wraps around a function to update the Firebase connection before the function's execution. It calls the `updateConnection` method of the instance (`self`) before proceeding with the original function call.

### Usage:

```python
from firebase_connection_decorator import update_connection_decorator

class FirebaseHandler:
    @update_connection_decorator
    def fetch_data(self, data_id):
        # Function to fetch data from Firebase
        pass

    def updateConnection(self):
        # Function to update the connection to Firebase
        pass
```