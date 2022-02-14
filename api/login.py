from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import db
from db import get_employee_from_token, get_employee_username
import jwt

with open("rsa_key.txt", "r") as f:
    global_secret = f.read()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def token_validity(token):
    try:
        user = jwt.decode(token, options={"verify_signature": False})
        hash_pass = db.get_employee_username(user['username'])['password']
        jwt.decode(token, f'{global_secret}{hash_pass}', algorithms=["HS256"])
        return True
    except jwt.exceptions.InvalidSignatureError as e:
        return False


def generate_token(user_dict):
    payload = {
        'username': user_dict['username'],
        'email': user_dict['email'],
        'name': user_dict['name']
    }

    hash_pass = user_dict['password']

    token = jwt.encode(payload, f'{global_secret}{hash_pass}', algorithm='HS256')

    return token


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    pass


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_employee_from_token(token=token)
    if not user and token_validity(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user['activated']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
