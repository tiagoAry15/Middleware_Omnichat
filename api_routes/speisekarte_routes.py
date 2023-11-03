# speisekarte.py
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from api_config.object_factory import fs
from aiohttp import web

# Funções assíncronas para lidar com as requisições

speisekarte_app = web.Application()
speisekarte_routes = web.RouteTableDef()


@speisekarte_routes.post('/create_menu')
async def create_menu(request):
    body_dict = await request.json()
    result = fs.createSpeisekarte(speisekarte_data=body_dict)
    if result:
        return web.json_response({"message": "Speisekarte created successfully"}, status=200)
    return web.json_response({"message": "Speisekarte already exists"}, status=200)


@speisekarte_routes.get('/get_menu_by_author/{author}')
async def get_menu_by_author(request):
    author = request.match_info['author']
    speisekarte_data = fs.read_speisekarte(author=author)
    if not speisekarte_data:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response(speisekarte_data, status=200)


@speisekarte_routes.put('/update_menu_by_author/{author}')
async def update_menu_by_author(request):
    author = request.match_info['author']
    body_dict = await request.json()
    result = fs.update_speisekarte(author=author, newData=body_dict)
    if not result:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response({"message": "Speisekarte updated successfully"}, status=200)


@speisekarte_routes.delete('/delete_menu_by_author/{author}')
async def delete_menu_by_author(request):
    author = request.match_info['author']
    result = fs.delete_speisekarte(author=author)
    if not result:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response({"message": "Speisekarte deleted successfully"}, status=200)


# Defina as rotas para a subaplicação
speisekarte_app.router.add_routes(speisekarte_routes)
