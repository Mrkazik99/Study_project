import asyncio

from starlette.responses import RedirectResponse
from typing import List, Optional
from fastapi import FastAPI, status, responses, Header, Cookie
from fastapi.middleware.cors import CORSMiddleware
import db
import jwt
import time

timeout = 60 * 15

sessions = [{'user': {'token': 'token', 'timeout': time.time()}},
            {'user': {'token': 'token', 'timeout': time.time()}}]


async def user_logout_task():
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
    if not check_and_update(x_token):
        return RedirectResponse(url='/')
    else:
        db.register(username, email, passwd)
        return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'account': 'registered'})


@app.get("/logout")
async def logout(x_token: Optional[List[str]] = Header(None)):
    if not check_and_update(x_token):
        return responses.Response(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        for index, session in enumerate(sessions):
            if x_token == session['user']['token']:
                del sessions[index]
                return responses.Response(status_code=status.HTTP_200_OK)
        return responses.Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/request/{req_id}")
async def request_id(req_id: int):
    res = db.get_request(req_id)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={'request': res})


@app.post("/create_request")
async def create_request(client_infos: dict, employee_id: int, description: str, new_customer: bool):
    db.create_request(client_infos, employee_id, description, new_customer)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_client")
async def create_client(client_infos: dict):
    db.create_customer(client_infos)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_department")
async def create_department(name: str):
    db.create_department(name=name)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_employee")
async def create_employee(employee_infos: dict):
    db.create_employee(employee_infos=employee_infos)
    return responses.Response(status_code=status.HTTP_201_CREATED)


asyncio.create_task(user_logout_task())
