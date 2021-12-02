from aiohttp import web
import aiohttp_cors
from db import Database
import jwt

db = Database()
routes = web.RouteTableDef()


@routes.get('/service/api/test')
async def test(request):
    return web.json_response({'accepted': True}, status=200)


@routes.get('/service/api/zadanko')
async def zadanko(request):
    return web.json_response({'Api': 'Odpowiada xDDD'}, status=200)


@routes.get('/service/api/get_customer')
async def zadanko(request):
    return web.json_response({"client": await db.get_data(request.rel_url.query['id'])}, status=200)


@routes.get('/service/api/push_customer')
async def zadanko(request):
    await db.push_data(request.rel_url.query['name'], request.rel_url.query['surname'], request.rel_url.query['phone'], request.rel_url.query['email'])
    return web.json_response({"status": "accepted"}, status=201)

@routes.post('/service/api/login')
async def login(request):
    login = request.rel_url.query['login']
    passwd = request.rel_url.query['passwd']
    result = await db.login(login, passwd)
    if result['result'] == 201:
        return web.json_response({'Status': 'Authorized'}, status=201)
    else:
        return web.json_response({'Status': 'Unauthorized'}, status=401)



app = web.Application()
app.add_routes(routes)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, host='0.0.0.0', port=80)

