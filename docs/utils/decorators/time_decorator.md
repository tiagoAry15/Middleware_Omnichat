## _time_decorator.py_
This module contains a decorator that measures the execution time of the decorated function and prints it to the console. Here are the functionalities it provides:

- `timingDecorator(func)`: A decorator that wraps around a function to measure its execution time. It calculates the time taken by the function to execute and prints a message with the function name and the execution time in seconds.

### Usage:

```python
from time_decorator import timingDecorator

@timingDecorator
def long_running_function():
    # Simulate a long-running function
    time.sleep(5)

# When the function is called, it will print the execution time to the console
long_running_function()
```