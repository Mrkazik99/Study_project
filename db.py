import asyncio
import sqlite3
from datetime import datetime

import psutil


class Database:
    def __init__(self):
        self.conn = conn = sqlite3.connect('./db/service.db')
        self.c = conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS employee(id integer PRIMARY KEY AUTOINCREMENT, username text,
        password text, first_name text, surname text, phone_number text, email text, address text,
        department_id integer)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS request(id integer PRIMARY KEY AUTOINCREMENT, id_employee integer,
        id_customer integer, description text, date0 datetime, date1 datetime, date2 datetime, status text, price float,
        department_id integer)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS customer(id integer PRIMARY KEY AUTOINCREMENT, first_name text,
        surname text, phone_number text, email text)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS department(id integer PRIMARY KEY AUTOINCREMENT, name text)""")

    async def get_data(self, user_id):
        for row in self.c.execute("""SELECT * FROM `customer` WHERE id=""" + str(user_id)):
            return row

    async def push_data(self, name, surname, phone, email):
        self.c.execute("INSERT INTO customer(first_name, surname, phone_number, email) VALUES (?, ?, ?, ?)",
                       (name, surname, phone, email))
        self.conn.commit()

    async def register(self, username, sha, email):
        self.c.execute("INSERT INTO employee(username, password, email) VALUES (?, ?, ?)", (username, sha, email))
        self.conn.commit()

    async def login(self, login, password, type='login'):
        if not login or not password:
            return {'result': 400}
        else:
            if type == 'login':
                if len(users := self.c.execute("SELECT username, password FROM employee WHERE username=?", login)) == 1:
                    user = None
                    for row in users:
                        user = row
                        break
                    if user[0] == login and user[0][1] == password:
                        return {'result': 201}
                else:
                    return {'result': 401}
            else:
                if len(users := self.c.execute("SELECT email, password FROM employee WHERE email=?", login)) == 1:
                    user = None
                    for row in users:
                        user = row
                        break
                    if user[0] == login and user[0][1] == password:
                        return {'result': 201}
                else:
                    return {'result': 401}

