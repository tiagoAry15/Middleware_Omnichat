import json
import os

import logging

from aiohttp import web

from api_config.api_setup import sio, cors, send_message
from api_config.core_factory import core_app
from api_config.object_factory import dialogflowConnectionManager
from api_config.cache_updater import ucm
from api_routes.speisekarte_routes import speisekarte_app
from api_routes.test_routes import test_app

from intentProcessing.core_intent_processing import fulfillment_processing

from utils import instagram_utils
from utils import core_utils
from utils.core_utils import create_message_json, process_bot_response, appendMultipleMessagesToFirebase, \
    sendMessageToUser

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

routes = web.RouteTableDef()
core_app.add_subapp('/speisekarte', speisekarte_app)
core_app.add_subapp('/test', test_app)


# Número máximo de tentativas de reenvio


@routes.get('/')
async def hello_world_endpoint():
    return web.Response(text="Hello, world!")


async def erase_session(request):
    if request.method != "PUT":
        return "This endpoint only accepts PUT requests", 405
    ip_address = request.remote_addr
    dialogflowConnectionManager.delete_session(ip_address)
    return "Session erased", 200


@routes.get('/instagram')
async def instagram_get(request):
    try:
        # Com aiohttp, você acessa os parâmetros da query com request.rel_url.query
        hub_mode = request.rel_url.query.get('hub.mode')
        hub_challenge = request.rel_url.query.get('hub.challenge')

        if hub_mode == 'subscribe' and hub_challenge:
            # O desafio enviado pelo Instagram deve ser retornado na resposta
            return web.Response(text=hub_challenge)
        else:
            # Em caso de requisição inválida, retorna-se o status 403
            return web.Response(text='Invalid Request', status=403)
    except Exception as e:
        # Em caso de exceção, imprime o erro e retorna status 500
        print(e)
        # Aqui se estiver usando logging, substitua por logging.error(str(e))
        return web.Response(text=str(e), status=500)


@routes.post('/instagram')
async def instagram_post(request):
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

            return web.Response(text=botResponse, content_type='text/plain')
    except Exception as e:
        print(e)
        logging.error(e)
        return web.Response(text=str(e), status=500, content_type='text/plain')


@routes.post('/twilioSandbox')
async def sandbox(request):
    try:
        userMessage, metaData = await core_utils.extract_data_fro_request(request)

        userMessageJSON = create_message_json(userMessage, metaData)
        existing_user = await ucm.check_existing_user_from_metadata(metaData=metaData)

        botResponse, BotResponseJSON = await process_bot_response(existing_user, userMessage, metaData, request)

        await send_message({'type': 'message', 'body': userMessageJSON})
        await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
        await send_message({'type': 'message', 'body': BotResponseJSON})
        return web.Response(text=botResponse, content_type='text/plain')

    except Exception as e:
        print(e)
        logging.error(e)
        return web.Response(text=str(e), status=500, content_type='text/plain')


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


core_app.add_routes(routes)

# Aplicar o CORS em todas as rotas, exceto as gerenciadas pelo socket.io
for route in list(core_app.router.routes()):

    path = route.resource.canonical
    if "/socket.io/" not in path:  # Exclui rotas do socket.io.
        cors.add(route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(core_app, host='0.0.0.0', port=port, shutdown_timeout=180)
