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
import api.datamodels
import json
import time

from api.login import generate_token, token_validity, User, remove_token

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    db.fill_db()
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'Done!'})


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_dict = db.get_employee(username=form_data.username, password=form_data.password)
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
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={}
        )


@app.get("/logout")
async def logout(user: User = Depends(check_token), authorization: str | None = Header(None)):
    if remove_token(authorization):
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not logout",
            headers={}
        )


@app.get("/get/request/{req_id}")
async def request_id(req_id: int, user: User = Depends(check_token)):
    res = db.get_request(req_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/customer/{customer_id}")
async def request_id(customer_id: int, user: User = Depends(check_token)):
    res = db.get_customer(customer_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.post("/create_request")
async def create_request(customer_id: int, employee_id: int, item: str, description: str, user: User = Depends(check_token)):
    db.create_request(customer_id, employee_id, item, description)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_customer")
async def create_client(name: str, phone: str, email: str, user: User = Depends(check_token)):
    db.create_customer(name, phone, email)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_department")
async def create_department(name: str, user: User = Depends(check_token)):
    db.create_department(name=name)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.post("/create_employee")
async def create_employee(uname: str, passwd: str, name: str, email: str, phone: str, dep_id: int, is_active: bool, user: User = Depends(check_token)):
    db.create_employee(username=uname, password=passwd, name=name, email=email, phone=phone, dep_id=dep_id, is_active=is_active)
    return responses.Response(status_code=status.HTTP_201_CREATED)


@app.get("/get/departments")
async def get_departments(user: User = Depends(check_token)):
    res = db.get_departments()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/customers")
async def get_customers(user: User = Depends(check_token)):
    res = db.get_customers()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/employees")
async def get_employees(user: User = Depends(check_token)):
    res = db.get_employees_departs()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/requests_date")
async def get_requests_date(scope=None, date_from1=None, date_to1=None, user: User = Depends(check_token)):
    date_from = datetime.now() - timedelta(days=30) if not date_from1 else datetime.strptime(date_from1, '%m/%d/%Y')
    date_to = datetime.now() if not date_to1 else datetime.strptime(date_to1 + "_23:59", '%m/%d/%Y_%H:%M')
    if datetime.timestamp(date_to) - datetime.timestamp(date_from) < 0:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)
    res = db.get_requests_date(date_from, date_to) if not scope else db.get_requests_date_and_scope(date_from, date_to, scope)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


asyncio.create_task(db.user_logout_task())