import subprocess

import requests
from utils.decorators.time_decorator import timingDecorator

NGROK_PATH = "C:\\Users\\Mateus\\Desktop\\ngrok.exe"


def open_ngrok():
    command = f'"{NGROK_PATH}" http 3000'

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: ngrok.exe not found. Make sure to provide the correct path.")


@timingDecorator
def get_ngrok_url():
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
    except requests.exceptions.ConnectionError:
        raise Exception("Error: ngrok is not running. Please run ngrok first.")
    if response:
        responseJson = response.json()
        return responseJson["tunnels"][0]["public_url"]
    return None


def __main():
    url = get_ngrok_url()
    # open_ngrok()
    return


if __name__ == "__main__":
    __main()
