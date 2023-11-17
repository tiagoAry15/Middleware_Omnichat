import urllib.parse

from locust import HttpUser, between, task
from mocks import mock_twilio_sandbox, mock_instagram_body, webhook_for_intent


class MyUser(HttpUser):
    wait_time = between(1, 2)  # O tempo de espera entre as requisições será entre 1 e 2 segundos

    @task
    def post_twilio_sandbox(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = mock_twilio_sandbox
        encoded_payload = urllib.parse.urlencode(payload)
        self.client.post("/twilioSandbox", data=encoded_payload, headers=headers)

    @task
    def post_instagram(self):
        headers = {'Content-Type': 'application/json'}
        payload = mock_instagram_body
        self.client.post("/instagram", json=payload, headers=headers)

    @task
    def post_webhook_for_intent(self):
        headers = {'Content-Type': 'application/json'}
        payload = webhook_for_intent
        self.client.post("/webhookForIntent", json=payload, headers=headers)

    @task
    def post_test_dialogflow(self):
        headers = {'Content-Type': 'application/json'}
        payload = 'teste'
        self.client.post("/testDialogflow", json=payload, headers=headers)
    @task
    def post_final_test(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = mock_twilio_sandbox
        encoded_payload = urllib.parse.urlencode(payload)
        self.client.post("/final_test", data=encoded_payload, headers=headers)