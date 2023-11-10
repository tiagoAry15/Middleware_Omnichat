import json
import os
import datetime

import aiohttp_cors
import socketio
import logging

from aiohttp import web
from flask import jsonify
from werkzeug.exceptions import BadRequest

from api_config.object_factory import dialogflowConnectionManager
from api_routes.speisekarte_routes import speisekarte_app
from dialogflowFolder.dialogflow_session import DialogflowSession
from intentProcessing.core_intent_processing import fulfillment_processing
from signupBot.whatsapp_handle_new_user import handleNewWhatsappUser
from signupBot.whatsapp_user_manager import check_existing_user_from_metadata
from utils import instagram_utils
from utils.core_utils import extractMetaDataFromTwilioCall, appendMultipleMessagesToFirebase

from utils.instagram_utils import extractMetadataFromInstagramDict
from utils.port_utils import get_ip_address_from_request

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
routes = web.RouteTableDef()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})


# redis = aioredis.from_url("redis://localhost")


async def get_room_from_cache(room):
    # Implemente a lógica para pegar o histórico de mensagens de uma sala
    return []


async def add_message_to_cache(room, message):
    # Implemente a lógica para adicionar uma mensagem ao cache
    pass


@sio.event
async def connect(sid, environ):
    print('Client connected', sid)


@sio.event
async def disconnect(sid):
    print('Client disconnected', sid)


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
                botResponse = await _get_bot_response_from_user_session(user_message=userMessage, ip_address=ip_address)
                await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse,
                                                       metaData=metaData)
            return web.json_response({'status': 'success', 'response': 'Message sent'}, status=400)
    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'status': 'failed', 'response': 'Message not sent'}, status=400)


async def _get_bot_response_from_user_session(user_message: str, ip_address: str) -> str:
    user_instance: DialogflowSession = dialogflowConnectionManager.get_instance_session(ip_address)

    # Inicializa a sessão, assumindo que 'initialize_session' não é uma coroutine
    user_instance.initialize_session(ip_address)

    # Aguarda a resposta da função assíncrona 'getDialogFlowResponse'
    response = await user_instance.getDialogFlowResponse(message=user_message)

    # Extrai o texto da resposta
    bot_answer: str = response.query_result.fulfillment_text

    return bot_answer


@routes.post('/twilioSandbox')
async def sandbox(request):
    try:
        data = await request.post()
        profile_name = data['ProfileName']
        print("TWILIO SANDBOX ENDPOINT!")
        metaData = extractMetaDataFromTwilioCall(data)
        existing_user = check_existing_user_from_metadata(metaData)
        if not existing_user:
            return web.json_response({'message': handleNewWhatsappUser(metaData)})
        ip_address = request.transport.get_extra_info('peername')[0]
        userMessage = str(data["Body"][0])
        userMessageJSON = {"body": userMessage, "timestamp": datetime.datetime.now().strftime('%d-%b-%Y %H:%M'),
                           **metaData}
        await sio.emit('message', {'message': userMessageJSON})
        botResponse = await _get_bot_response_from_user_session(user_message=userMessage, ip_address=ip_address)
        await appendMultipleMessagesToFirebase(userMessage=userMessage, botAnswer=botResponse, metaData=metaData)
        BotResponseJSON = {"body": botResponse, "timestamp": datetime.datetime.now().strftime('%d-%b-%Y %H:%M'),
                           **metaData,
                           "sender": "Bot"}
        await sio.emit('message', {'message': BotResponseJSON})
        return web.json_response({'message': botResponse})
    except Exception as e:
        print(e)
        logging.error(e)
        return web.json_response({'message': 'Message not sent', 'error': e}, status=400)


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
        logging.error(e)
        return web.Response(text='Erro no processamento de resposta do Bot, tente novamente em instantes!', status=500)


@routes.post('/testDialogflow')
async def dialogflow_testing(request):
    if request.method != "POST":
        return web.Response(text=json.dumps({"message": "This endpoint only accepts POST requests"}), status=405,
                            content_type='application/json')
    try:
        body = await request.json()
        ip_address = get_ip_address_from_request(request)
        bot_answer = await _get_bot_response_from_user_session(user_message=body, ip_address=ip_address)
        # bot_answer = {
        #     "source": "dialogFlow",
        #     "fulfillmentText": "Olá! Bem-vindo à Pizza do Bill! Funcionamos das 17h às 22h.\n Cardápio de pizzas:"
        #                        "\n- Calabresa - R$17.50\n- Frango - R$18.90\n- Portuguesa - R$13.99\n- Margherita -"
        #                        " R$15.50\n- Quatro Queijos - R$16.90\n- Pepperoni - R$19.99\n. \nQual pizza você"
        #                        " vai querer?",
        #     "outputContexts": [
        #         {
        #             "name": "projects/catupirybase/locations/global/agent/sessions/859e5892-b2c2-6027-0334-00c"
        #                     "272efcbf4/contexts/Start",
        #             "lifespanCount": 1,
        #             "parameters": {}
        #         }
        #     ]
        # }
        if bot_answer == "":
            return web.Response(text=json.dumps({"message": f"Could not find any response from Dialogflow for the "
                                                            f"message '{body}'. Check if your message is valid."}),
                                status=400, content_type='application/json')
        return web.Response(text=json.dumps(bot_answer), status=200, content_type='application/json')
    except Exception as e:
        return web.Response(text=json.dumps({"message": str(e)}), status=500, content_type='application/json')


app.add_routes(routes)
app.add_subapp('/speisekarte', speisekarte_app)

# Aplicar o CORS em todas as rotas, exceto as gerenciadas pelo socket.io
for route in list(app.router.routes()):

    path = route.resource.canonical
    if "/socket.io/" not in path:  # Exclui rotas do socket.io.
        cors.add(route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, host='0.0.0.0', port=port, shutdown_timeout=180)
