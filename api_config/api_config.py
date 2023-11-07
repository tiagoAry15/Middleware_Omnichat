import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
twilio_account_ssid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
twilioClient = Client(twilio_account_ssid, twilio_auth_token)


