import os

from dotenv import load_dotenv
from twilio.rest import Client


def initialize_twilio_client():
    load_dotenv()
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    return Client(account_sid, auth_token)


def __list_phone_numbers():
    client = initialize_twilio_client()

    # Fetch all the phone numbers associated with your account
    phone_numbers = client.incoming_phone_numbers.list()

    for phone in phone_numbers:
        print(f"Phone Number: {phone.phone_number} | SID: {phone.sid}")


def __list_messaging_services():
    client = initialize_twilio_client()

    # List all messaging services associated with your account
    services = client.messaging.services.list()

    for service in services:
        print(f"Service Name: {service.friendly_name} | Service SID: {service.sid}")


def update_whatsapp_sandbox_webhook(new_url: str = "https://facebook.com"):
    client = initialize_twilio_client()

    # List all phone numbers to find the WhatsApp one
    phone_numbers = client.incoming_phone_numbers.list()

    whatsapp_number_sid = None
    for number in phone_numbers:
        if "whatsapp:" in number.phone_number:
            whatsapp_number_sid = number.sid
            break

    if not whatsapp_number_sid:
        print("WhatsApp number not found!")
        return

    # Update the webhook URL for the found WhatsApp phone number
    client.incoming_phone_numbers(whatsapp_number_sid).update(sms_url=new_url)

    print(f"Updated WhatsApp Sandbox Webhook to: {new_url}")


def __main():
    update_whatsapp_sandbox_webhook()
    return


if __name__ == "__main__":
    __main()
