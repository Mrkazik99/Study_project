import asyncio
import sqlite3
from datetime import datetime

import psutil


class Database:
    def __init__(self):
        self.conn = conn = sqlite3.connect('./db/service.db')
        self.c = conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS employee(id integer PRIMARY KEY AUTOINCREMENT, username text,
        password text, first_name text, surname text, phone_number text, email text, address text)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS request(id integer PRIMARY KEY AUTOINCREMENT, id_employee integer,
        id_customer integer, description text, date0 datetime, date1 datetime, dat2 datetime, status text)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS customer(id integer PRIMARY KEY AUTOINCREMENT, first_name text,
        surname text, phone_number text, email text)""")

    async def get_data(self, user_id):
        for row in self.c.execute("""SELECT * FROM `customer` WHERE id="""+str(user_id)):
            return row

    async def push_data(self, name, surname, phone, email):
        self.c.execute("INSERT INTO customer(first_name, surname, phone_number, email) VALUES (?, ?, ?, ?)", (name, surname, phone, email))
        self.conn.commit()

