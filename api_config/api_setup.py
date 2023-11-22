import time
import datetime
import os

import asyncio
import uuid

import aiohttp_cors
import socketio
from aiohttp import web
from dotenv import load_dotenv
from twilio.rest import Client
from api_config.core_factory import core_app


load_dotenv()
twilio_account_ssid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = f'whatsapp:{os.environ["TWILIO_PHONE_NUMBER"]}'
twilio_fb_page_id = f'messenger:{os.environ["TWILIO_FB_PAGE_ID"]}'
twilioClient = Client(twilio_account_ssid, twilio_auth_token)

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
sio.attach(core_app)
pending_messages = {}
connected_users = {}

ACK_TIMEOUT = 10  # Tempo limite para aguardar confirmação (em segundos)
MAX_RETRIES = 3


cors = aiohttp_cors.setup(core_app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})



@sio.event
async def connect(sid, environ):
    print('Client connected', sid)
    connected_users[sid] = sid


@sio.event
async def disconnect(sid):
    print('Client disconnected', sid)
    if sid in connected_users:
        del connected_users[sid]


async def send_message(message):
    message_id = str(uuid.uuid4())
    message['id'] = message_id

    # Armazenar informações da mensagem
    pending_messages[message_id] = {
        'type': message['type'],
        'body': message['body'],
        'timestamp': str(datetime.datetime.now()),
        'attempts': 0
    }

    # Enviar a mensagem e iniciar o processo de verificação
    await attempt_send_message(message_id)


async def attempt_send_message(message_id):
    if message_id in pending_messages:
        msg_info = pending_messages[message_id]
        msg_info['id'] = message_id
        if msg_info['attempts'] < MAX_RETRIES:
            await sio.emit(msg_info['type'], msg_info)
            msg_info['attempts'] += 1
            asyncio.create_task(wait_for_ack(message_id))


async def wait_for_ack(message_id):
    await asyncio.sleep(ACK_TIMEOUT)
    if message_id in pending_messages:
        await attempt_send_message(message_id)


@sio.on('message_ack')
async def message_ack(sid, data):
    print('Message ack', data)
    message_id = data['id']
    if message_id in pending_messages:
        del pending_messages[message_id]


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    web.run_app(core_app, port=5000)