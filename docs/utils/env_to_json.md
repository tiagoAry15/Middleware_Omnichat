## _env_to_json.py_

This module is responsible for converting environment variables stored in a `.env` file to a JSON format. It reads the `.env` file line by line, extracts the key-value pairs of environment variables, and writes them to a JSON file. Here are the functionalities provided by this module:

### Functions

- **convert_env_to_json(env_file, json_file)**: This function takes the paths of the `.env` file and the destination JSON file as inputs. It reads the `.env` file line by line, ignoring lines that are either empty or start with a '#' (comments). It then extracts the key-value pairs and writes them to the JSON file in a formatted manner. After the conversion, it prints a message indicating the successful conversion.

- **__main()**: A function that demonstrates the usage of the `convert_env_to_json` function. It retrieves the paths of the `.env` and `.json` files using functions from the `path_reference` module and then calls `convert_env_to_json` with these paths as arguments.

### Usage

This module is used to convert environment variables from a `.env` file to a JSON file, facilitating easier management and utilization of environment variables in different parts of the application.

### Examples

The `__main__` function within the module provides a demonstration of how to use the `convert_env_to_json` function with paths retrieved from the `path_reference` module.

```python
env_file_path = getEnvPath()
json_file_path = getTokenJsonPath()

convert_env_to_json(env_file_path, json_file_path)
```

### Results
Upon successful execution, the script will print a message indicating the successful conversion of the .env file to the JSON file, mentioning the paths of both files.