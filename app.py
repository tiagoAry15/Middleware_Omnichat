import asyncio
import json
import os
import datetime
import uuid

import aiohttp_cors
import socketio
import logging
from urllib.parse import unquote
from aiohttp import web

from api_config.api_config import app
from api_config.object_factory import dialogflowConnectionManager
from api_routes.speisekarte_routes import speisekarte_app
from intentProcessing.core_intent_processing import fulfillment_processing
from signupBot.whatsapp_handle_new_user import handleNewWhatsappUser
from signupBot.whatsapp_user_manager import check_existing_user_from_metadata
from utils import instagram_utils
from utils.core_utils import extractMetaDataFromTwilioCall, appendMultipleMessagesToFirebase, create_message_json, \
    process_bot_response
from utils.dialogflow_utils import get_bot_response_from_session, create_session

from utils.instagram_utils import extractMetadataFromInstagramDict
from utils.port_utils import get_ip_address_from_request

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
sio.attach(app)
routes = web.RouteTableDef()
ACK_TIMEOUT = 10  # Tempo limite para aguardar confirmação (em segundos)
MAX_RETRIES = 3
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})
app.add_subapp('/speisekarte', speisekarte_app)

pending_messages = {}
connected_users = {}  # Número máximo de tentativas de reenvio


async def send_message(message):
    message_id = str(uuid.uuid4())
    message['id'] = message_id

    # Armazenar informações da mensagem
    pending_messages[message_id] = {
        'message': message,
        'timestamp': datetime.datetime.now(),
        'attempts': 0
    }

    # Enviar a mensagem e iniciar o processo de verificação
    await attempt_send_message(message_id)


async def attempt_send_message(message_id):
    if message_id in pending_messages:
        msg_info = pending_messages[message_id]
        if msg_info['attempts'] < MAX_RETRIES:
            await sio.emit('message', msg_info['message'])
            msg_info['attempts'] += 1
            asyncio.create_task(wait_for_ack(message_id))


async def wait_for_ack(message_id):
    await asyncio.sleep(ACK_TIMEOUT)
    if message_id in pending_messages:
        await attempt_send_message(message_id)


@sio.on
async def message_ack(sid, data):
    print('Message ack', data)
    message_id = data['id']
    if message_id in pending_messages:
        del pending_messages[message_id]


async def get_room_from_cache(room):
    # Implemente a lógica para pegar o histórico de mensagens de uma sala
    return []


async def add_message_to_cache(room, message):
    # Implemente a lógica para adicionar uma mensagem ao cache
    pass


@sio.event
async def connect(sid, environ):
    print('Client connected', sid)
    connected_users[sid] = sid


@sio.event
async def disconnect(sid):
    print('Client disconnected', sid)
    if sid in connected_users:
        del connected_users[sid]


@routes.post('/test')
async def post_endpoint(request):
    data = await request.json()

    await sio.emit('notification', {'message': 'Received POST data'})
    return web.json_response({'message': 'Data received', 'data': data})


@routes.get('/')
async def hello_world_endpoint(request):
    return web.Response(text="Hello, world!")


async def erase_session(request):
    if request.method != "PUT":
        return "This endpoint only accepts PUT requests", 405
    ip_address = request.remote_addr
    dialogflowConnectionManager.erase_session(ip_address)
    return "Session erased", 200


@routes.post('/instagram')
async def instagram(request):
    try:
        if request.method == 'GET':
            if request.args.get('hub.mode') == 'subscribe':
                return request.args.get('hub.challenge')
            else:
                return 'Invalid Request', 403
        if request.method == 'POST':
            # Handle POST requests here (i.e. updates from Instagram)
            data = request.get_json()
            headers = list(request.headers)
            ip_address = request.remote_addr
            is_echo = data['entry'][0]['messaging'][0]['message'].get('is_echo')
            if not is_echo:
                properMessage: dict = instagram_utils.convertIncomingInstagramMessageToProperFormat(data)
                metaData = extractMetadataFromInstagramDict(properMessage)
                userMessage = str(properMessage["Body"][0])
                loop = asyncio.get_running_loop()
                session = create_session(ip_address)
                botResponse = await loop.run_in_executor(None,
                                                         get_bot_response_from_session,
                                                         session, userMessage)
                await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse,
                                                       metaData=metaData)
            return web.json_response({'status': 'success', 'response': 'Message sent'}, status=400)
    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'status': 'failed', 'response': 'Message not sent'}, status=400)


@routes.post('/twilioSandbox')
async def sandbox(request):
    try:
        data = await request.post()
        print("TWILIO SANDBOX ENDPOINT!")
        unquoted_dict = {k: unquote(v) if isinstance(v, str) else v for k, v in request.headers.items()}
        dictData = {**dict(data), **unquoted_dict}
        metaData = extractMetaDataFromTwilioCall(dictData)
        userMessage = metaData["userMessage"]
        userMessageJSON = create_message_json(userMessage, metaData)

        # Verificar se o usuário já existe
        existing_user = await check_existing_user_from_metadata(metaData)

        # Processar a resposta do bot
        botResponse, BotResponseJSON = await process_bot_response(existing_user, userMessage, metaData, request)

        # Enviar mensagens e salvar no Firebase
        await send_message({'message': userMessageJSON})
        await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
        await send_message({'message': BotResponseJSON})

        return web.json_response({'message': botResponse})
    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'message': 'Message not sent', 'error': str(e)}, status=400)


@routes.post('/webhookForIntent')
async def webhookForIntent(request):
    try:
        requestContent = await request.json()
        response_content = await fulfillment_processing(requestContent)
        if isinstance(response_content, str):
            response_content = json.loads(response_content)
        print(f"fulfillment webhook response: {response_content}")
        return web.json_response(response_content)
    except Exception as e:
        logging.exception(e)
        return web.Response(text='Erro no processamento de resposta do Bot, tente novamente em instantes!', status=500)


@routes.post('/testDialogflow')
async def dialogflow_testing(request):
    content_type = 'application/json;'
    if request.method != "POST":
        return web.Response(text=json.dumps({"message": "This endpoint only accepts POST requests"}), status=405,
                            content_type=content_type)
    try:
        body = await request.json()
        ip_address = get_ip_address_from_request(request)
        loop = asyncio.get_running_loop()
        session = create_session(ip_address)
        bot_answer = await loop.run_in_executor(None,
                                                 get_bot_response_from_session,
                                                 session, body)
        if bot_answer == "":
            return web.Response(text=json.dumps({"message": f"Could not find any response from Dialogflow for the "
                                                            f"message '{body}'. Check if your message is valid."}),
                                status=400, content_type=content_type)
        return web.Response(text=json.dumps(bot_answer, ensure_ascii=False), status=200, content_type=content_type)
    except Exception as e:
        logging.exception(e)
        return web.Response(text=json.dumps({"message": str(e)}), status=500, content_type=content_type)


app.add_routes(routes)


# Aplicar o CORS em todas as rotas, exceto as gerenciadas pelo socket.io
for route in list(app.router.routes()):

    path = route.resource.canonical
    if "/socket.io/" not in path:  # Exclui rotas do socket.io.
        cors.add(route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, host='0.0.0.0', port=port, shutdown_timeout=180)
