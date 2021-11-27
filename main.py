from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/smtool/api/v0.1/platform')
async def platform_info(request):

    return web.json_response({'accepted': True}, status=200)


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=80)