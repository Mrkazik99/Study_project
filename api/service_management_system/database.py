from decimal import Decimal
from pony.orm import *
from datetime import datetime, timedelta
from service_management_system import IS_DEV
import os
import jwt
import asyncio

db = Database()


class Department(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    workers = Set('Employee')


class Employee(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    password = Required(str)
    department = Required(Department)
    activated = Required(bool)
    admin_permissions = Required(bool)
    token = Optional(str)
    name = Optional(str)
    phone_number = Optional(str)
    requests = Set('Request')
    composite_key(username, email)


class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    phone_number = Required(int)
    email = Optional(str)
    requests = Set('Request')


class Request(db.Entity):
    id = PrimaryKey(int, auto=True)
    employee = Required(Employee)
    customer = Required(Customer)
    item = Required(str)
    description = Required(str)
    status = Required(int)
    date0 = Required(datetime)
    date1 = Required(datetime)
    date2 = Optional(datetime)
    price = Optional(Decimal)


if IS_DEV:
    if os.name == "nt":
        print("Detected windows OS")
        db.bind(provider='sqlite', filename='service.db', create_db=True)
    else:
        print("Detected unix based OS")
        db.bind(provider='sqlite', filename='./db/service.db', create_db=True)
else:
    db.bind(provider='mysql', host='service_db', user='service_user', passwd='6EgF48arFnP7Ew', db='service_database')
db.generate_mapping(create_tables=True)


# set_sql_debug(True)


def token_date(token):
    return jwt.decode(token, options={"verify_signature": False})['date']


async def user_logout_task():
    while True:
        print(f'{datetime.now()} -- checking for inactive users')
        iterate_tokens()
        await asyncio.sleep(600)


@db_session
def iterate_tokens():
    for user in select(user for user in Employee):
        print('user')
        if user.token != '':
            if datetime.now() - datetime.strptime(token_date(user.token), '%m/%d/%Y_%H:%M:%S') >= timedelta(
                    minutes=9999):
                print(f'outdated token for {user.username}')
                user.token = ''
                db.commit()
    db.flush()


@db_session
def initialize(admin_uname: str, admin_email: str, admin_passwd: str, department_name: str, real_name: str):
    if not Department.select().exists():
        department = Department(name=department_name)
        db.flush()
        Employee(username=admin_uname, email=admin_email,
                 password=admin_passwd,
                 department=department, activated=True, admin_permissions=True, token='', name=real_name)
        db.flush()
        return True
    else:
        return False


#  ----------------------->Requests section<-----------------------

@db_session
def create_request(customer_id: int, employee_id: int, item: str, description: str):
    try:
        Request(employee=Employee.get(id=employee_id), customer=Customer.get(id=customer_id), item=item,
                description=description, status=1, date0=datetime.now(), date1=datetime.now())
        db.flush()
        return True
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def update_request(req_id: int, employee=None, description=None, date2=None, status=None, price=None):
    try:
        req = Request.get(id=req_id)
        req.employee = Employee.get(id=employee) if employee else req.employee
        req.description = description if description else req.description
        req.date1 = datetime.now()
        req.date2 = date2 if date2 else req.date2
        req.status = status if status else req.status
        req.price = price if price else req.price
        db.flush()
        return True
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def get_request_by_id(req_id: int):
    try:
        result = Request.get(id=req_id).to_dict()
        result['customer'] = Customer.get(id=result['customer']).to_dict()
        result['employee'] = Employee.get(id=result['employee']).to_dict()
        result['date0'] = datetime.strftime(result['date0'], '%m/%d/%Y')
        result['date1'] = datetime.strftime(result['date1'], '%m/%d/%Y')
        result['date2'] = datetime.strftime(result['date2'], '%m/%d/%Y') if result['date2'] else None
        return result
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_requests_by_person(customer_id: int):
    try:
        result = [row.to_dict() for row in
                  select(req for req in Request if Request.customer == Customer.get(id=customer_id))]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
        return result
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_requests_by_dates(start, end):
    try:
        result = [row.to_dict() for row in select(req for req in Request if req.date0 >= start and req.date0 <= end)]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
            req['date0'] = datetime.strftime(req['date0'], '%m/%d/%Y')
            req['date1'] = datetime.strftime(req['date1'], '%m/%d/%Y')
        return result
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_requests_by_date_and_employee(start, end, user):
    try:
        result = [row.to_dict() for row in select(req for req in Request if
                                                  req.date0 >= start and req.date0 <= end and req.employee == Employee.get(
                                                      username=user))]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
            req['date0'] = datetime.strftime(req['date0'], '%m/%d/%Y')
            req['date1'] = datetime.strftime(req['date1'], '%m/%d/%Y')
        return result
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_requests_by_dates_and_customer(start, end, customer_name):
    try:
        result = [row.to_dict() for row in select(req for req in Request if
                                                  req.date0 >= start and req.date0 <= end and req.customer == Customer.get(
                                                      name=customer_name))]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
            req['date0'] = datetime.strftime(req['date0'], '%m/%d/%Y')
            req['date1'] = datetime.strftime(req['date1'], '%m/%d/%Y')
        return result
    except Exception as e:
        print('Result not found', e)
        return None


#  ----------------------->Customers section<-----------------------

@db_session
def create_customer(name, phone, email):
    try:
        Customer(name=name, phone_number=phone, email=email)
        db.flush()
        return True
    except Exception as e:
        print('Could not create row', e)
        return False


@db_session
def update_customer(customer_id, name, phone, email):
    try:
        customer = Customer.get(id=customer_id)
        customer.name = name if name else customer.name
        customer.phone_number = phone if phone else customer.phone
        customer.email = email if email else customer.email
        db.flush()
        return True
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def get_customer(customer_id):
    try:
        return Customer.get(id=customer_id).to_dict()
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_customers():
    return [row.to_dict() for row in select(req for req in Customer)]


#  ----------------------->Employees section<-----------------------


@db_session
def create_employee(uname: str, password: str, name: str, email: str, phone: str, dep_id: int, active: bool,
                    admin: bool):
    try:
        Employee(username=uname, password=password, email=email, phone_number=phone, name=name,
                 department=Department.get(id=dep_id), activated=active, admin_permissions=admin)
        db.flush()
        return True
    except Exception as e:
        print('Could not create row', e)
        return False


@db_session
def update_employee(employee_id, email, department_id, activated, admin, name, phone):
    try:
        employee = Employee.get(id=employee_id)
        employee.name = name if name else employee.name
        employee.phone = phone if phone else employee.phone
        employee.email = email if email else employee.email
        employee.department = Department.get(id=department_id) if department_id else employee.department
        employee.activated = activated
        employee.admin_permissions = admin
        db.flush()
        return True
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def update_password_hash_for_user(name: str, passwd: str):
    try:
        employee = Employee.get(username=name)
        employee.password = passwd
        db.flush()
        return True
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def update_employee_token(username: str, token: str):
    try:
        employee = Employee.get(username=username)
        employee.token = token
        db.flush()
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def get_employee_by_id(employee_id: int):
    try:
        result = Employee.get(id=employee_id).to_dict()
        result['department'] = Department.get(id=result['department']).to_dict()
        return result
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_employee_by_username(username: str):
    try:
        return Employee.get(username=username).to_dict()
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_employee_from_token(token: str):
    try:
        return Employee.get(token=token).to_dict()
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_employees():
    return [row.to_dict() for row in select(req for req in Employee)]


@db_session
def get_employees_with_departs():
    result = [row.to_dict() for row in select(req for req in Employee)]
    for employee in result:
        employee['department'] = Department.get(id=employee['department']).to_dict()['name']
    return result


#  ----------------------->Departments section<-----------------------

@db_session
def update_department(id: int, name: str):
    try:
        department = Department.get(id=id)
        department.name = name
        db.flush()
    except Exception as e:
        print('Could not update row', e)
        return False


@db_session
def create_department(department: str):
    try:
        Department(name=department)
        db.flush()
        return True
    except Exception as e:
        print('Could not create row', e)
        return False


@db_session
def get_department(department_id: int):
    try:
        return Department.get(id=department_id).to_dict()
    except Exception as e:
        print('Result not found', e)
        return None


@db_session
def get_departments():
    return [row.to_dict() for row in select(req for req in Department)]
