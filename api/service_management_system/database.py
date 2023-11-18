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
def fill_db():
    Department(name='administracja')
    db.flush()
    Employee(username='worker1', email='abc1@abc.pl',
             password='fbacf4a44108031458024d7528c0a6e08ccd91f9c2b42d4d39f514d6db2a7ad893fac14038bec2512300af67e871d39163dcaf0bf0ff532986f10a9f5ba85314',
             department=Department[1], activated=True, admin_permissions=True,
             token='', name='worker1')
    Customer(name='customer1', phone_number='123123123')
    db.flush()
    for i in range(2):
        Request(employee=Employee[1], customer=Customer[1], item="Samsung", description='mgikomndfgo', status=1,
                date0=datetime.now(),
                date1=datetime.now())
    db.flush()


@db_session
def initialize():
    if not Department.select().exists():
        Department(name='administracja')
        db.flush()
        Employee(username='admin', email='admin@admin.pl',
                 password='fbacf4a44108031458024d7528c0a6e08ccd91f9c2b42d4d39f514d6db2a7ad893fac14038bec2512300af67e871d39163dcaf0bf0ff532986f10a9f5ba85314',
                 department=Department[1], activated=True, admin_permissions=True, token='', name='admin')
        db.flush()
        return True
    else:
        return False


#  ----------------------->Auth section<-----------------------

@db_session
def register(username: str, email: str, passwd: str):
    department = Department.get(id=1)
    if department is None:
        department = Department(name='administracja')
        db.flush()
    employee = Employee(username=username, email=email, password=passwd, department=department, activated=False)
    db.flush()


@db_session
def is_employee(username: str, password: str):
    try:
        return Employee.exists(username=username, password=password)
    except Exception as e:
        raise Exception('Something is wrong') from e


@db_session
def insert_employee(username: str, email: str, passwd: str, department_id: int):
    department = Department.get(id=department_id)
    employee = Employee(username=username, email=email, password=passwd, department=department)
    db.flush()


#  ----------------------->Requests section<-----------------------

@db_session
def create_request_db(customer_id: int, employee_id: int, item: str, description: str):
    try:
        Request(employee=Employee.get(id=employee_id), customer=Customer.get(id=customer_id), item=item,
                description=description, status=1, date0=datetime.now(), date1=datetime.now())
        db.flush()
        return True
    except Exception as e:
        raise Exception('Something is wrong') from e


@db_session
def update_request_db(req_id: int, employee=None, description=None, date2=None, status=None, price=None):
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
        raise Exception('Something is wrong') from e


@db_session
def get_request(req_id: int):
    try:
        result = Request.get(id=req_id).to_dict()
        result['customer'] = Customer.get(id=result['customer']).to_dict()
        result['employee'] = Employee.get(id=result['employee']).to_dict()
        result['date0'] = datetime.strftime(result['date0'], '%m/%d/%Y')
        result['date1'] = datetime.strftime(result['date1'], '%m/%d/%Y')
        result['date2'] = datetime.strftime(result['date2'], '%m/%d/%Y') if result['date2'] else None
        return result
    except Exception as e:
        raise Exception('Something is wrong') from e


@db_session
def get_requests_person(customer_id: int):
    try:
        result = [row.to_dict() for row in
                  select(req for req in Request if Request.customer == Customer.get(id=customer_id))]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
        return result
    except Exception as e:
        raise Exception('Something is wrong') from e


@db_session
def get_requests_date(start, end):
    try:
        result = [row.to_dict() for row in select(req for req in Request if req.date0 >= start and req.date0 <= end)]
        for req in result:
            req['customer'] = Customer.get(id=req['customer']).to_dict()['name']
            req['employee'] = Employee.get(id=req['employee']).to_dict()['name']
            req['date0'] = datetime.strftime(req['date0'], '%m/%d/%Y')
            req['date1'] = datetime.strftime(req['date1'], '%m/%d/%Y')
        return result
    except Exception as e:
        return None


@db_session
def get_requests_date_and_scope(start, end, user):
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
        return None


#  ----------------------->Customers section<-----------------------

@db_session
def create_customer_db(name, phone, email):
    try:
        Customer(name=name, phone_number=phone, email=email)
        db.flush()
        return True
    except TransactionIntegrityError:
        return False


@db_session
def update_customer_db(customer_id, name, phone, email):
    try:
        customer = Customer.get(id=customer_id)
        customer.name = name if name else customer.name
        customer.phone_number = phone if phone else customer.phone
        customer.email = email if email else customer.email
        db.flush()
        return True
    except Exception as e:
        raise Exception('Something is wrong') from e


@db_session
def get_customer(customer_id):
    return Customer.get(id=customer_id).to_dict()


@db_session
def get_customers():
    return [row.to_dict() for row in select(req for req in Customer)]


#  ----------------------->Employees section<-----------------------

@db_session
def create_employee_db(uname: str, password: str, name: str, email: str, phone: str, dep_id: int, active: bool,
                       admin: bool):
    try:
        Employee(username=uname, password=password, email=email, phone_number=phone, name=name,
                 department=Department.get(id=dep_id), activated=active, admin_permissions=admin)
        db.flush()
        return True
    except TransactionIntegrityError:
        return False


@db_session
def update_employee_db(employee_id, email, department_id, activated, admin, name, phone):
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
        raise Exception('Something is wrong') from e


@db_session
def put_employee_token(username: str, token: str):
    employee = Employee.get(username=username)
    employee.token = token
    db.flush()


@db_session
def get_employee(username: str, password: str):
    try:
        return Employee.get(username=username, password=password).to_dict()
    except Exception as e:
        return None


@db_session
def get_employee_by_id(employee_id: int):
    try:
        result = Employee.get(id=employee_id).to_dict()
        result['department'] = Department.get(id=result['department']).to_dict()
        return result
    except Exception as e:
        return None


@db_session
def get_employee_username(username: str):
    try:
        return Employee.get(username=username).to_dict()
    except Exception as e:
        return None


@db_session
def get_employee_from_token(token: str):
    try:
        return Employee.get(token=token).to_dict()
    except Exception as e:
        return None


@db_session
def get_employees():
    return [row.to_dict() for row in select(req for req in Employee)]


@db_session
def get_employees_departs():
    result = [row.to_dict() for row in select(req for req in Employee)]
    for employee in result:
        employee['department'] = Department.get(id=employee['department']).to_dict()['name']
    return result


#  ----------------------->Departments section<-----------------------

@db_session
def create_department_db(department: str):
    try:
        Department(name=department)
        db.flush()
        return True
    except TransactionIntegrityError:
        return False


@db_session
def get_department(department_id: int):
    return Department.get(id=department_id).to_dict()


@db_session
def get_departments():
    result = []
    for row in select(req for req in Department):
        result.append(row.to_dict())
    return result
