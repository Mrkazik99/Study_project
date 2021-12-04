from decimal import Decimal
from pony.orm import *
from datetime import datetime

db = Database()


class Department(db.Entity):
    name = Required(str)


class Employee(db.Entity):
    username = Required(str)
    email = Required(str)
    password = Required(str)
    department_id = Required(Department)
    first_name = Optional(str)
    surname = Optional(str)
    phonr_number = Optional(str)


class Customer(db.Entity):
    first_name = Required(str)
    surname = Required(str)
    phonr_number = Required(str)
    email = Optional(str)


class Request(db.Entity):
    id_employee = Required(Employee)
    id_customer = Required(Customer)
    description = Required(str)
    date0 = Required(datetime)
    date1 = Optional(datetime)
    date2 = Optional(datetime)
    status = Optional(int)
    price = Optional(Decimal)


db.bind(provider='sqlite', filename='./db/service.db', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(True)

@db_session
def insert_employee(username: str, email: str, passwd: str, department_id: int):
    p1 = Employee(username=username, email=email, password=passwd, department_id=department_id)
    commit()

@db_session
def get_employee():
    result = select(employee for employee in Employee)[:]
    return result

while True:
    print('1')