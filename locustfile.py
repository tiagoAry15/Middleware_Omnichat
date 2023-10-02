import urllib.parse

from locust import HttpUser, between, task
from mocks import mock_twilio_sandbox


class MyUser(HttpUser):
    wait_time = between(1, 2)  # O tempo de espera entre as requisições será entre 1 e 2 segundos

    @task
    def post_twilio_sandbox(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = mock_twilio_sandbox
        encoded_payload = urllib.parse.urlencode(payload)
        self.client.post("/twilioSandbox", data=encoded_payload, headers=headers)
