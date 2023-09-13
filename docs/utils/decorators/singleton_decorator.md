## _singleton_decorator.py_
This module contains a decorator that ensures a class follows the singleton pattern, meaning that only one instance of the class can exist. Here are the functionalities it provides:

- `singleton(cls)`: A decorator that modifies a class to follow the singleton pattern. It keeps track of instances created and returns the existing instance if one has already been created for the specified class.

### Usage:

```python
from singleton_decorator import singleton

@singleton
class SingletonClass:
    def __init__(self, value):
        self.value = value

# Usage
instance1 = SingletonClass(1)
instance2 = SingletonClass(2)

assert instance1 is instance2  # This will be True, demonstrating the singleton behavior
```