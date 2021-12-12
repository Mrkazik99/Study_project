import asyncio

from starlette.responses import RedirectResponse
from typing import List, Optional
from fastapi import FastAPI, status, responses, Header, Cookie
from fastapi.middleware.cors import CORSMiddleware
import db
import jwt
import time

timeout = 60 * 15

sessions = [{'user': {'token': 'token', 'timeout': 'timeout'}},
            {'user': {'token': 'token', 'timeout': 'timeout'}}]


async def user_logout():
    while True:
        for index, session in enumerate(sessions):
            if time.time() - session['user']['timeout'] > timeout:
                del session[index]
        await asyncio.sleep(60)


def check_and_update(token):
    for index, session in enumerate(sessions):
        if token == session['user']['token']:
            # signature comparison here
            session['user']['timeout'] = time.time()
            return True
        else:
            return False


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'Hello world!'})


@app.get("/login")
async def login(username, passwd, username_login):
    if db.login(username, passwd, username_login)['auth']:
        # generate token and pass it to browser
        ...
    else:
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={'credentials': 'wrong'})


@app.post("/register")
async def register(username, passwd, email, x_token: Optional[List[str]] = Header(None)):
    if check_and_update(x_token):
        return RedirectResponse(url='/')
    else:
        db.register(username, email, passwd)
        return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'account': 'registered'})


@app.get("/request/{req_id}")
async def request_id(req_id: int):
    res = db.get_request(req_id)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={'requests': res})


loop = asyncio.get_running_loop()
loop.run_until_complete(user_logout())
