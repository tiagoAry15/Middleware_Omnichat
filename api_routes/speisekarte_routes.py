from aiohttp import web


# Cria um objeto encaminhador para gerenciar as rotas
speisekarte_routes = web.RouteTableDef()
speisekarte_app = web.Application()


# Funções assíncronas para lidar com as requisições

@speisekarte_routes.post('/create_menu')

async def create_menu(request):
    from api_config.object_factory import fs
    body_dict = await request.json()
    result = fs.createSpeisekarte(speisekarte_data=body_dict)
    if result:
        return web.json_response({"message": "Speisekarte created successfully"}, status=200)
    return web.json_response({"message": "Speisekarte already exists"},
                             status=409)  # Use 409 Conflict for already existing resource


@speisekarte_routes.get('/get_menu_by_author/{author}')

async def get_menu_by_author(request):
    from api_config.object_factory import fs
    author = request.match_info['author']
    speisekarte_data = fs.read_speisekarte(author=author)
    if not speisekarte_data:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response(speisekarte_data, status=200)


@speisekarte_routes.put('/update_menu_by_author/{author}')
async def update_menu_by_author(request):
    from api_config.object_factory import fs
    author = request.match_info['author']
    body_dict = await request.json()
    result = fs.update_speisekarte(author=author, newData=body_dict)
    if not result:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response({"message": "Speisekarte updated successfully", "speisekarte": result}, status=200)


@speisekarte_routes.delete('/delete_menu_by_author/{author}')
async def delete_menu_by_author(request):
    from api_config.object_factory import fs
    author = request.match_info['author']
    result = fs.deleteSpeisekarte(author=author)
    if not result:
        return web.json_response({"message": "Speisekarte not found"}, status=404)
    return web.json_response({"message": "Speisekarte deleted successfully"}, status=200)


speisekarte_app.add_routes(speisekarte_routes)
