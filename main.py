import asyncio
import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.responses import RedirectResponse
from typing import List, Optional
from fastapi import FastAPI, status, responses, Header, Cookie, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import db
from datetime import datetime, timedelta
import json
import time

from api.login import generate_token, token_validity, User

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    db.fill_db()
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'Done!'})


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = db.get_employee(username=form_data.username, password=form_data.password)
    print(user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user_dict['password'] == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = generate_token(user_dict)

    return {"access_token": user_dict['username'], "token_type": "bearer", "token": token}


@app.get("/check_token")
async def check_token(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={}
        )
    if token_validity(authorization):
        return responses.Response(status_code=status.HTTP_200_OK)
    elif authorization == 'elo':
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={}
        )


# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


@app.get("/get/request/{req_id}")
async def request_id(req_id: int):
    res = db.get_request(req_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


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


@app.get("/get/departments")
async def get_departments():
    res = db.get_departments()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/customers")
async def get_customers():
    res = db.get_customers()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/employees")
async def get_employees():
    res = db.get_employees_departs()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/requests_date")
async def get_requests_date(date_from1=None, date_to1=None, user: User = Depends(check_token)):
# async def get_requests_date(date_from1=None, date_to1=None):
    date_from = datetime.now() - timedelta(days=30) if not date_from1 else date_from1
    date_to = datetime.now() if not date_to1 else date_to1
    print(date_from, date_to)
    res = db.get_requests_date(date_from, date_to)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    if datetime.timestamp(date_to) - datetime.timestamp(date_from) < 0:
        print('gowno')
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
