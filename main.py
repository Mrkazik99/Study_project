from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/test')
async def test():

    return web.json_response({'accepted': True}, status=200)

@routes.get('/zadanko')
async def zadanko():

    return web.json_response({'Api': 'Odpowiada xDDD'}, status=200)


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=80)
