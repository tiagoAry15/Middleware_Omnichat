import asyncio
import json
import os

import logging

from aiohttp import web

from api_config.api_setup import sio, cors, send_message
from api_config.api_core_app_instance import core_app
from api_config.object_factory import dialogflowConnectionManager, ucm
from api_routes.speisekarte_routes import speisekarte_app

from intentProcessing.core_intent_processing import fulfillment_processing

from utils import instagram_utils
from utils import core_utils
from utils.core_utils import create_message_json, process_bot_response, appendMultipleMessagesToFirebase, \
    sendMessageToUser
from utils.dialogflow_utils import get_bot_response_from_session, create_dialogflow_session

from utils.port_utils import get_ip_address_from_request

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

routes = web.RouteTableDef()
core_app.add_subapp('/speisekarte', speisekarte_app)


# Número máximo de tentativas de reenvio


async def get_room_from_cache(room):
    # Implemente a lógica para pegar o histórico de mensagens de uma sala
    return []


async def add_message_to_cache(room, message):
    # Implemente a lógica para adicionar uma mensagem ao cache
    pass


@routes.post('/test')
async def post_endpoint(request):
    data = await request.json()

    await sio.emit('notification', {'message': 'Received POST data'})
    return web.json_response({'message': 'Data received', 'data': data})


@routes.get('/')
async def hello_world_endpoint():
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

            userMessage, metaData = await instagram_utils.extract_data_from_request(request)

            userMessageJSON = create_message_json(userMessage, metaData)
            existing_user = await ucm.check_existing_user_from_metadata(metaData=metaData)

            botResponse, BotResponseJSON = await core_utils.process_bot_response(existing_user, userMessage, metaData)
            await send_message({'type': 'message', 'body': userMessageJSON})
            await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
            await send_message({'type': 'message', 'body': BotResponseJSON})

            return web.json_response({'status': 'success', 'response': 'Message sent'}, status=200)
    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'status': 'failed', 'response': 'Message not sent'}, status=400)


@routes.post('/twilioSandbox')
async def sandbox(request):
    try:
        userMessage, metaData = await core_utils.extract_data_fro_request(request)

        userMessageJSON = create_message_json(userMessage, metaData)
        existing_user = await ucm.check_existing_user_from_metadata(metaData=metaData)

        botResponse, BotResponseJSON = await process_bot_response(existing_user, userMessage, metaData)

        await send_message({'type': 'message', 'body': userMessageJSON})
        await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
        await send_message({'type': 'message', 'body': BotResponseJSON})
        return web.json_response({'message': botResponse})

    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'message': 'Message not sent', 'error': str(e)}, status=400)


@routes.post('/webhookForIntent')
async def webhookForIntent(request):
    try:
        requestContent = await request.json()
        requestContent["ip"] = requestContent['session'].split('/')[-1]
        response_content = await fulfillment_processing(requestContent)
        if isinstance(response_content, str):
            response_content = json.loads(response_content)
        print(f"fulfillment webhook response: {response_content}")
        return web.json_response(response_content)
    except Exception as e:
        logging.exception(e)
        return web.Response(text='Erro no processamento de resposta do Bot, tente novamente em instantes!', status=500)


@routes.post('/send_message_to_user/{user_number}')
async def send_message_to_user(request):
    try:
        if request.method == 'OPTIONS':
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "3600",
            }

            return '', 204, headers
        user_number = request.match_info['user_number']
        message = await request.json()

        if not user_number:
            return web.json_response(data={'error': "Field user_number cannot be empty"}, status=400)

        if not message:
            return web.json_response(data={'error': "Message cannot be empty"}, status=400)
        response = await sendMessageToUser(message, user_number)
        return web.json_response(data=response, status=200)

    except Exception as e:
        return web.json_response(data={'error': str(e)}, status=500)


@routes.post('/socket_sending_order')
async def socket_sending_order(request):
    try:
        if request.method == 'OPTIONS':
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "3600",
            }

            return '', 204, headers

        orderObject = await request.json()
        response = await send_message({'type': 'order', 'body': orderObject})
        return web.json_response(data=response, status=200)

    except Exception as e:
        return web.json_response(data={'error': str(e)}, status=500)


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
        session = create_dialogflow_session(ip_address)
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


@routes.post('/final_test')
async def final_test(request):
    userMessage, metaData = await core_utils.extract_data_fro_request(request)
    userMessageJSON = create_message_json(userMessage, metaData)

    # Verificar se o usuário já existe
    existing_user = await ucm.check_existing_user_from_metadata(metaData=metaData)

    # Processar a resposta do bot
    botResponse, BotResponseJSON = await process_bot_response(existing_user, userMessage, metaData)
    # Enviar mensagens e salvar no Firebase
    await send_message({'type': 'message', 'body': userMessageJSON})
    await asyncio.sleep(0.5)
    await send_message({'type': 'message', 'body': BotResponseJSON})

    return web.json_response({'message': botResponse}, status=200)


core_app.add_routes(routes)

# Aplicar o CORS em todas as rotas, exceto as gerenciadas pelo socket.io
for route in list(core_app.router.routes()):

    path = route.resource.canonical
    if "/socket.io/" not in path:  # Exclui rotas do socket.io.
        cors.add(route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(core_app, host='0.0.0.0', port=port, shutdown_timeout=180)
