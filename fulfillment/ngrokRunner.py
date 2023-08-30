import atexit
import subprocess
import requests
import time

ngrok_path = "C:\\Users\\Mateus\\Desktop\\ngrok.exe"


class NgrokManager:
    def __init__(self):
        self.process = None

    def start_ngrok(self, port=3000, delay_time=5):
        """Starts ngrok and returns the public URL."""
        self.process = subprocess.Popen([ngrok_path, "http", str(port)])

        # Give ngrok some time to establish the tunnel
        time.sleep(delay_time)

        # Get the public URL
        response = requests.get("http://localhost:4040/api/tunnels")
        json_data = response.json()

        public_url = ""
        for tunnel in json_data["tunnels"]:
            if tunnel['proto'] == 'https':
                public_url = tunnel['public_url']
                break

        print(f"Public URL: {public_url}")
        return public_url

    def close_ngrok(self):
        """Closes the ngrok process if it's running."""
        if self.process:
            self.process.terminate()


def __main():
    ngrok_instance = NgrokManager()
    atexit.register(ngrok_instance.close_ngrok)
    public_url = ngrok_instance.start_ngrok(3000)
    return


if __name__ == "__main__":
    __main()
