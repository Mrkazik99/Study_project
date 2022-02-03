from decimal import Decimal
from pony.orm import *
from datetime import datetime
import os
import json

db = Database()


class Department(db.Entity):
    name = Required(str)
    workers = Set('Employee')


class Employee(db.Entity):
    username = Required(str)
    email = Required(str)
    password = Required(str)
    department = Required(Department)
    activated = Required(bool)
    name = Optional(str)
    phone_number = Optional(str)
    requests = Set('Request')


class Customer(db.Entity):
    name = Required(str)
    phone_number = Required(str)
    email = Optional(str)
    requests = Set('Request')


class Request(db.Entity):
    employee = Required(Employee)
    customer = Required(Customer)
    description = Required(str)
    status = Required(int)
    date0 = Required(datetime)
    date1 = Optional(datetime)
    date2 = Optional(datetime)
    price = Optional(Decimal)


if os.name == "nt":
    print("Detected windows OS")
    db.bind(provider='sqlite', filename='service.db', create_db=True)
else:
    print("Detected unix based OS")
    db.bind(provider='sqlite', filename='./db/service.db', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(True)


@db_session(serializable=False)
def fill_db():
    Department(name='administracja')
    db.flush()
    Employee(username='worker1', email='abc@abc.pl', password='hard_password', department=Department[1], activated=True)
    Customer(name='customer1', phone_number='123123123')
    db.flush()
    for i in range(2):
        Request(employee=Employee[1], customer=Customer[1], description='mgikomndfgo', status=0, date0=datetime.now())
    db.flush()


#  ----------------------->Auth section<-----------------------

@db_session()
def register(username: str, email: str, passwd: str):
    department = Department.get(id=1)
    if department is None:
        department = Department(name='administracja')
        db.flush()
    employee = Employee(username=username, email=email, password=passwd, department=department, activated=False)
    db.flush()


@db_session()
def put_token(token, user):
    ...


@db_session()
def login(username: str, passwd: str, username_login: bool):
    if username_login:
        user = Employee.select(lambda e: e.username == username)
        if user == 1:
            if passwd == user.password:
                return {'auth': True}
            else:
                return {'auth': False}
        else:
            return {'auth': False}
    else:
        user = Employee.select(lambda e: e.email == username)
        if user == 1:
            if passwd == user.password:
                return {'auth': True}
            else:
                return {'auth': False}
        else:
            return {'auth': False}


@db_session()
def insert_employee(username: str, email: str, passwd: str, department_id: int):
    department = Department.get(id=department_id)
    employee = Employee(username=username, email=email, password=passwd, department=department)
    db.flush()


@db_session(serializable=True)
def get_employee():
    result = []
    for row in select(employee for employee in Employee):
        result.append(row.to_dict())

    x = [row.to_dict() for row in select(employee for employee in Employee)]
    return x


#  ----------------------->Requests section<-----------------------

@db_session()
def create_request(customer_infos: dict, employee_id: int, description: str, new_customer: bool):
    if new_customer:
        customer = Customer(name=customer_infos['name'], phone_number=customer_infos['phone'],
                            email=customer_infos['mail'])
    else:
        customer = Customer.get(id=customer_infos['id'])

    r = Request(employee=Employee.get(id=employee_id), customer=customer, description=description,
                status=0, date0=datetime.now)
    db.flush()


@db_session()
def update_request(req_id: int, employee=None, customer=None, description=None, date0=None, date1=None, date2=None,
                   status=None, price=None):
    req = Request.get(id=req_id)
    req.employee = employee if employee else req.employee
    req.customer = customer if customer else req.customer
    req.description = description if description else req.description
    req.date0 = date0 if date0 else req.date0
    req.date1 = date1 if date1 else req.date1
    req.date2 = date2 if date2 else req.date2
    req.status = status if status else req.status
    req.price = price if price else req.price
    db.flush()
        
        
@db_session(serializable=True)
def get_request(req_id: int):
    request = Request.get(id=req_id)
    return request.to_dict()


@db_session(serializable=True)
def get_requests_person(customer_id: int):
    result = []
    for row in select(req for req in Request if Request.customer == Customer.get(id=customer_id)):
        result.append(row.to_dict())
    return result


@db_session(serializable=True)
def get_requests_date(start, end):
    result = []
    for row in select(req for req in Request if Request.date0 >= start and Request.date0 <= end):
        result.append(row.to_dict())
    return result


@db_session()
def remove_request():
    ...


#  ----------------------->Customers section<-----------------------

@db_session()
def create_customer(customer_infos):
    customer = Customer(name=customer_infos['name'], phone_number=customer_infos['phone'], email=customer_infos['mail'])
    db.flush()


@db_session()
def update_customer():
    ...


@db_session(serializable=True)
def get_customer():
    ...


@db_session(serializable=True)
def get_customers():
    result = []
    for row in select(req for req in Customer):
        result.append(row.to_dict())
    return result


@db_session()
def remove_customer():
    ...


#  ----------------------->Employees section<-----------------------

@db_session()
def create_employee(employee_infos: dict):
    employee = Employee(username=employee_infos['user'], password=employee_infos['passwd'],
                        email=employee_infos['mail'], department=Department.get(id=employee_infos['department_id']))
    db.flush()


@db_session()
def update_employee():
    ...


@db_session(serializable=True)
def get_employee():
    ...


@db_session(serializable=True)
def get_employees():
    result = []
    for row in select(req for req in Employee):
        result.append(row.to_dict())
    return result


@db_session(serializable=True)
def get_employees_departs():
    result = []
    for row in select(req for req in Employee):
        result.append(row.to_dict())
    for employee in result:
        employee['department'] = Department.get(id=employee['department']).to_dict()['name']
    return result


@db_session()
def remove_employee():
    ...


#  ----------------------->Departments section<-----------------------

@db_session()
def create_department(department: str):
    department = Department(name=department)
    db.flush()


@db_session(serializable=True)
def get_department(department_id: int):
    department = Department.get(id=department_id)
    return department.to_dict()


@db_session(serializable=True)
def get_departments():
    result = []
    for row in select(req for req in Department):
        result.append(row.to_dict())
    return result


@db_session(serializable=True)
def remove_department():
    ...
