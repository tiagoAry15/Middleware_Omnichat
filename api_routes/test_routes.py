# routes/conversation_routes.py
import json

import asyncio
import logging

from aiohttp import web

from api_config.api_setup import send_message
from api_config.cache_updater import ucm
from utils import core_utils
from utils.core_utils import create_message_json, process_bot_response
from utils.dialogflow_utils import create_dialogflow_session, get_bot_response_from_session
from utils.port_utils import get_ip_address_from_request

test_routes = web.RouteTableDef()
test_app = web.Application()

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')


@test_routes.post('/socket_sending_order')
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


@test_routes.post('/testDialogflow')
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
        session.metaData = {
            "from": request.headers.get("From"),
            "name": request.headers.get("ProfileName"),
            "phoneNumber":request.headers.get("From").split(":")[1],
            "address": request.headers.get("Address"),
        }
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


@test_routes.post('/final_test')
async def final_test(request):
    userMessage, metaData = await core_utils.extract_data_fro_request(request)
    userMessageJSON = create_message_json(userMessage, metaData)

    # Verificar se o usuário já existe
    existing_user = await ucm.check_existing_user_from_metadata(metaData=metaData)

    # Processar a resposta do bot
    botResponse, BotResponseJSON = await process_bot_response(existing_user, userMessage, metaData, request)
    # Enviar mensagens e salvar no Firebase
    await send_message({'type': 'message', 'body': userMessageJSON})
    await asyncio.sleep(2.0)
    await send_message({'type': 'message', 'body': BotResponseJSON})

    return web.json_response({'message': botResponse}, status=200)

test_app.add_routes(test_routes)