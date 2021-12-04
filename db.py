from decimal import Decimal
from pony.orm import *
from datetime import datetime

db = Database()


class Department(db.Entity):
    name = Required(str)
    workers = Optional('Employee', reverse='department_id')


class Employee(db.Entity):
    username = Required(str)
    email = Required(str)
    password = Required(str)
    department_id = Optional(Department)
    first_name = Optional(str)
    surname = Optional(str)
    phone_number = Optional(str)
    requests = Optional('Request', reverse='id_employee')


class Customer(db.Entity):
    first_name = Required(str)
    surname = Required(str)
    phone_number = Required(str)
    email = Optional(str)
    requests = Optional('Request', reverse='id_customer')


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
def insert_employee(username: str, email: str, passwd: str):
    p1 = Employee(username=username, email=email, password=passwd)
    commit()

@db_session
def get_employee():
    result = select(employee for employee in Employee)[:]
    return result
