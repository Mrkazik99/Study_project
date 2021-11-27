from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/service/api/test')
async def test(request):
    return web.json_response({'accepted': True}, status=200)


@routes.get('/service/api/zadanko')
async def zadanko(request):
    return web.json_response({'Api': 'Odpowiada xDDD'}, status=200)


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=80)
