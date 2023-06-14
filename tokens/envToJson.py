import os
import json

from references.pathReference import getEnvPath, getTokenJsonPath


def convert_env_to_json(env_file, json_file):
    data = {}

    with open(env_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                data[key] = value

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Converted {env_file} to {json_file}")


def __main():
    # Provide the paths of your .env and .json files
    env_file_path = getEnvPath()
    json_file_path = getTokenJsonPath()

    convert_env_to_json(env_file_path, json_file_path)


if __name__ == '__main__':
    __main()
