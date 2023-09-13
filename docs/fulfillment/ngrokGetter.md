## ngrokGetter.py

This module is responsible for interacting with the ngrok application to facilitate the retrieval of the public URL exposed by ngrok and optionally initiating the ngrok process. Here are the primary functionalities of this module:

- **Opening ngrok**: The `open_ngrok` function can initiate the ngrok process, opening a tunnel to the local host at port 3000. The path to the ngrok executable is specified in the `NGROK_PATH` constant.
- **Fetching the ngrok URL**: The `get_ngrok_url` function, decorated with the `timingDecorator` to measure its execution time, fetches the public URL exposed by ngrok by interacting with the ngrok API.

### Usage

To use this module, simply run the script. It will automatically execute the `__main__` function, which calls the `get_ngrok_url` function to retrieve the ngrok public URL. The `open_ngrok` function is commented out in the `__main__` function but can be uncommented if you wish to initiate the ngrok process from within the script.

### Functions

- `open_ngrok()`: This function initiates the ngrok process, opening a tunnel to the local host at port 3000. It utilizes the `subprocess` module to run the ngrok command. The path to the ngrok executable is specified in the `NGROK_PATH` constant.

- `get_ngrok_url()`: This function fetches the public URL exposed by ngrok by sending a GET request to the ngrok API. It returns the public URL as a string. If ngrok is not running, it raises an exception.

- `__main__()`: This function calls the `get_ngrok_url` function to retrieve the ngrok public URL. It also contains a commented-out call to the `open_ngrok` function, which can be uncommented to initiate the ngrok process from within the script.

### Decorators

- `timingDecorator`: This decorator is used to measure the execution time of the `get_ngrok_url` function. It is imported from the `utils.decorators.time_decorator` module.

### Constants

- `NGROK_PATH`: This constant holds the path to the ngrok executable. It is used in the `open_ngrok` function to specify the ngrok executable to run.

### Error Handling

The script contains error handling to manage potential issues that might occur during the execution, such as ngrok not being found at the specified path or ngrok not running when attempting to fetch the public URL.

Ensure to have the necessary modules and dependencies installed and the ngrok executable available at the specified path before running the script.
