import asyncio
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, status, responses, Header, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
import service_management_system.database as database
from datetime import timedelta
from service_management_system.datamodels import *

from service_management_system.login import generate_token, token_validity, User, remove_token

close_statuses = [4, 5]

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    print(f'{datetime.now()} -- db_fill called')
    database.fill_db()
    return responses.JSONResponse({}, status_code=status.HTTP_201_CREATED)


@app.get("/admin/initialize")
async def initialize():
    print(f'{datetime.now()} -- Calling initialization')
    init_app = database.initialize()
    if init_app:
        print(f'{datetime.now()} -- APP has been initialized')
        return responses.Response(status_code=status.HTTP_201_CREATED)
    else:
        print(f'{datetime.now()} -- APP initialization failed')
        return responses.JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                      content={'message': 'APP has been already initialized'})


@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_dict = database.get_employee(username=form_data.username, password=form_data.password)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user_dict['activated']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user_dict['password'] == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = generate_token(user_dict)

    response.set_cookie(key="Authorization", value=token)

    # return responses.JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": user_dict['username'], "token_type": "bearer", "token": token})
    return RedirectResponse(url='http://localhost/dashboard.html', status_code=status.HTTP_302_FOUND)


@app.get("/check_token")
async def check_token(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={}
        )
    if token_validity(authorization):
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={}
        )


@app.get("/logout")
async def logout(user: User = Depends(check_token), authorization: str | None = Header(None)):
    if remove_token(authorization):
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not logout",
            headers={}
        )


@app.get("/get/request/{req_id}")
async def request_id(req_id: int, user: User = Depends(check_token)):
    res = database.get_request(req_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/customer/{cust_id}")
async def customer_id(cust_id: int, user: User = Depends(check_token)):
    res = database.get_customer(cust_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/employee/{emp_id}")
async def employee_id(emp_id: int, user: User = Depends(check_token)):
    res = database.get_employee_by_id(emp_id)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.post("/create/request")
async def create_request(request: NewRequest = Depends(NewRequest.as_form), user: User = Depends(check_token)):
    res = database.create_request_db(request.id_customer, request.id_employee, request.item, request.description)
    if res:
        return responses.Response(status_code=status.HTTP_201_CREATED)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/create/customer")
async def create_client(customer: NewCustomer = Depends(NewCustomer.as_form), user: User = Depends(check_token)):
    res = database.create_customer_db(customer.name, customer.phone_number, customer.email)
    if res:
        return responses.Response(status_code=status.HTTP_201_CREATED)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/create/department")
async def create_department(department: NewDepartment = Depends(NewDepartment.as_form),
                            user: User = Depends(check_token)):
    res = database.create_department_db(department.name)
    if res:
        return responses.Response(status_code=status.HTTP_201_CREATED)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/create/employee")
async def create_employee(employee: NewEmployee = Depends(NewEmployee.as_form), user: User = Depends(check_token)):
    is_admin = True if employee.admin_permissions else False
    res = database.create_employee_db(employee.username, employee.password, employee.name, employee.email,
                                      employee.phone_number,
                                      employee.department_id, employee.activated, is_admin)
    if res:
        return responses.Response(status_code=status.HTTP_201_CREATED)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/update/request")
async def update_request(request: EditRequest = Depends(EditRequest.as_form), user: User = Depends(check_token)):
    if status in close_statuses:
        date2 = datetime.now()
    else:
        date2 = None
    res = database.update_request_db(request.id_entity, request.employee, request.description, date2, request.status,
                                     request.price)
    if res:
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/update/customer")
async def update_client(customer: EditCustomer = Depends(EditCustomer.as_form), user: User = Depends(check_token)):
    res = database.update_customer_db(customer.id_entity, customer.name, customer.phone_number, customer.email)
    if res:
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/update/employee")
async def update_employee(employee: EditEmployee = Depends(EditEmployee.as_form), user: User = Depends(check_token)):
    res = database.update_employee_db(employee.id_entity, employee.email, employee.department, employee.activated,
                                      employee.admin_permissions, employee.name, employee.phone_number)
    if res:
        return responses.Response(status_code=status.HTTP_200_OK)
    else:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/get/departments")
async def get_departments(user: User = Depends(check_token)):
    res = database.get_departments()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/customers")
async def get_customers(user: User = Depends(check_token)):
    res = database.get_customers()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.get("/get/employees")
async def get_employees(user: User = Depends(check_token)):
    res = database.get_employees_departs()
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


@app.post("/edit/employee")
async def edit_employee(payload: EditEmployee):
    new_payload = {}


@app.get("/get/requests_date")
async def get_requests_date(scope=None, date_from1=None, date_to1=None, user: User = Depends(check_token)):
    date_from = datetime.now() - timedelta(days=30) if not date_from1 else datetime.strptime(date_from1, '%m/%d/%Y')
    date_to = datetime.now() if not date_to1 else datetime.strptime(date_to1 + "_23:59", '%m/%d/%Y_%H:%M')
    if datetime.timestamp(date_to) - datetime.timestamp(date_from) < 0:
        return responses.Response(status_code=status.HTTP_400_BAD_REQUEST)
    res = database.get_requests_date(date_from, date_to) if not scope else database.get_requests_date_and_scope(
        date_from, date_to,
        scope)
    if not res:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    json_compatible_res = jsonable_encoder(res)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)


asyncio.create_task(database.user_logout_task())
