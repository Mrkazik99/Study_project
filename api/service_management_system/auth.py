import datetime
from service_management_system.database import update_employee_token, get_employee_by_username
import jwt
import argon2

with open("./rsa_key.txt", "r") as f:
    global_secret = f.read()

ph = argon2.PasswordHasher()


def token_validity(token):
    try:
        print(token)
        user = jwt.decode(token.encode(), options={"verify_signature": False})
        user = get_employee_by_username(user['username'])
        print(user.token)
        if user.token:
            hash_pass = user.password
            jwt.decode(token, f'{global_secret}{hash_pass}{user["date"]}', algorithms=["HS256"])
            if get_employee_by_username(username=user['username'])['token'] == token:
                return True
            else:
                return False
        else:
            return False
    except jwt.exceptions.InvalidSignatureError as e:
        return False
    except Exception as e:
        print(e)
        return False


def generate_token(user_dict):
    payload = {
        'username': user_dict['username'],
        'email': user_dict['email'],
        'name': user_dict['name'],
        'date': datetime.datetime.now().strftime('%m/%d/%Y_%H:%M:%S'),
        'admin': user_dict['admin_permissions']
    }

    hash_pass = user_dict['password']

    token = jwt.encode(payload, f'{global_secret}{hash_pass}{payload["date"]}', algorithm='HS256')

    update_employee_token(user_dict['username'], token)

    return token


def remove_token(token):
    try:
        if token_validity(token):
            user = jwt.decode(token, options={"verify_signature": False})['username']
            update_employee_token(user, '')
            return True
        else:
            return False
    except Exception as e:
        return False


def hash_password(passwd: str):
    hashed_passwd = ph.hash(passwd)
    return hashed_passwd


def verify_hashes(hash_passwd: str, passwd: str):
    try:
        ph.verify(hash_passwd, passwd)
        if ph.check_needs_rehash(hash_passwd):
            return True, ph.hash(passwd)
        return True, None
    except argon2.exceptions.VerifyMismatchError:
        return False, None