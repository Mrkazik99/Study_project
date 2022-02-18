import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import put_employee_token, get_employee_username
import jwt

with open("rsa_key.txt", "r") as f:
    global_secret = f.read()

app = FastAPI()



def token_validity(token):
    try:
        user = jwt.decode(token, options={"verify_signature": False})
        hash_pass = get_employee_username(user['username'])['password']
        jwt.decode(token, f'{global_secret}{hash_pass}{user["date"]}', algorithms=["HS256"])
        if get_employee_username(username=user['username'])['token'] == token:
            return True
        else:
            return False
    except jwt.exceptions.InvalidSignatureError as e:
        return False
    except Exception as e:
        print(e)


def generate_token(user_dict):
    payload = {
        'username': user_dict['username'],
        'email': user_dict['email'],
        'name': user_dict['name'],
        'date': datetime.datetime.now().strftime('%m/%d/%Y_%H:%M:%S')
    }

    hash_pass = user_dict['password']

    token = jwt.encode(payload, f'{global_secret}{hash_pass}{payload["date"]}', algorithm='HS256')

    put_employee_token(user_dict['username'], token)

    return token


def remove_token(token):
    user = jwt.decode(token, options={"verify_signature": False})['username']
    put_employee_token(user, '')
    return True


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
