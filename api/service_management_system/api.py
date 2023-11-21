import asyncio
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, status, Header, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import service_management_system.database as database
from datetime import timedelta, datetime
import service_management_system.api_datamodels as datamodels
from service_management_system.utils import get_utc_date

from service_management_system.auth import generate_token, token_validity, remove_token, global_secret, hash_password, \
    verify_hashes

close_statuses = [4, 5]

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/admin/initialize', status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {
        'description': 'Success',
        'model': datamodels.BasicMessage
    },
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized',
        'model': datamodels.BasicMessage
    },
    status.HTTP_409_CONFLICT: {
        'description': 'Conflict',
        'model': datamodels.BasicMessage
    }
})
async def admin_initialize(key=""):
    if key == global_secret:
        init_app = database.initialize(admin_uname='admin', admin_email='admin@admin.pl',
                                       admin_passwd=hash_password('asdfg123Aq'), department_name='administracja',
                                       real_name='admin')
        if init_app:
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={'message': 'App initialized successfully'})
        else:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                content={'message': 'APP has been already initialized'})
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'message': 'Not authorized to initialize APP'})


@app.post("/login", status_code=status.HTTP_302_FOUND, responses={
    status.HTTP_302_FOUND: {
        'description': 'Success',
        'model': datamodels.BasicMessage
    },
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Bad request',
        'model': datamodels.LoginMessage
    }
})
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Incorrect username or password'})
    user_dict = database.get_employee_by_username(username=form_data.username)
    if not user_dict:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Incorrect username or password'})
    if not user_dict['activated']:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Incorrect username or password'})
    verify_password = verify_hashes(passwd=form_data.password, hash_passwd=user_dict['password'])
    if not verify_password[0]:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Incorrect username or password'})
    if verify_password[-1]:
        database.update_password_hash_for_user(user_dict['username'], verify_password[-1])

    token = generate_token(user_dict)

    return JSONResponse(status_code=status.HTTP_302_FOUND, content={'login_status': 'success',
                                                                    'token_type': 'Bearer',
                                                                    'token_data': token})


@app.get("/checklogintoken", status_code=status.HTTP_302_FOUND, responses={
    status.HTTP_302_FOUND: {
        'description': 'Success',
        'model': datamodels.RedirectMessage
    },
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized',
        'model': datamodels.RedirectMessage
    },
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Bad request',
        'model': datamodels.RedirectMessage
    }
})
async def check_login_token(authorization: str | None = Header(None)):
    if not authorization:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'redirect_url': 'http://localhost/login'}
        )
    if token_validity(authorization):
        return JSONResponse(status_code=status.HTTP_302_FOUND, content={'redirect_url': 'http://localhost/dashboards'})
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={'redirect_url': 'http://localhost/login'})


@app.get("/checktoken", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {
        'description': 'Success',
        'model': datamodels.BasicMessage
    },
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized',
        'model': datamodels.RedirectMessage
    },
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Bad request',
        'model': datamodels.RedirectMessage
    }
})
async def check_token(authorization: str | None = Header(None)):
    if not authorization:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'redirect_url': 'http://localhost/login'}
        )
    if token_validity(authorization):
        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Token valid'})
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={'redirect_url': 'http://localhost/login'})


@app.get("/logout", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {
        'description': 'Success',
        'model': datamodels.RedirectMessage
    },
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Unauthorized',
        'model': datamodels.RedirectMessage
    }
})
async def logout(authorization: str | None = Header(None)):
    if remove_token(authorization):
        return JSONResponse(status_code=status.HTTP_200_OK, content={'redirect_url': 'http://localhost/logout'})
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={'redirect_url': 'http://localhost/login'}
        )


# @app.get("/get/request/{req_id}")
# async def request_id(req_id: int, user: datamodels.User = Depends(check_token)):
#     res = database.get_request_by_id(req_id)
#     if not res:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.get("/get/customer/{cust_id}")
# async def customer_id(cust_id: int, user: datamodels.User = Depends(check_token)):
#     res = database.get_customer(cust_id)
#     if not res:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.get("/get/employee/{emp_id}")
# async def employee_id(emp_id: int, user: datamodels.User = Depends(check_token)):
#     res = database.get_employee_by_id(emp_id)
#     if not res:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.post("/create/request")
# async def create_request(request: datamodels.NewRequest = Depends(datamodels.NewRequest.as_form),
#                          user: datamodels.User = Depends(check_token)):
#     res = database.create_request(request.id_customer, request.id_employee, request.item, request.description)
#     if res:
#         return Response(status_code=status.HTTP_201_CREATED)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/create/customer")
# async def create_client(customer: datamodels.NewCustomer = Depends(datamodels.NewCustomer.as_form),
#                         user: datamodels.User = Depends(check_token)):
#     res = database.create_customer(customer.name, customer.phone_number, customer.email)
#     if res:
#         return Response(status_code=status.HTTP_201_CREATED)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/create/department")
# async def create_department(department: datamodels.NewDepartment = Depends(datamodels.NewDepartment.as_form),
#                             user: datamodels.User = Depends(check_token)):
#     res = database.create_department(department.name)
#     if res:
#         return Response(status_code=status.HTTP_201_CREATED)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/create/employee")
# async def create_employee(employee: datamodels.NewEmployee = Depends(datamodels.NewEmployee.as_form),
#                           user: datamodels.User = Depends(check_token)):
#     is_admin = True if employee.admin_permissions else False
#     res = database.create_employee(employee.username, employee.password, employee.name, employee.email,
#                                    employee.phone_number,
#                                    employee.department_id, employee.activated, is_admin)
#     if res:
#         return Response(status_code=status.HTTP_201_CREATED)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/update/request")
# async def update_request(request: datamodels.EditRequest = Depends(datamodels.EditRequest.as_form),
#                          user: datamodels.User = Depends(check_token)):
#     if status in close_statuses:
#         date2 = datetime.now()
#     else:
#         date2 = None
#     res = database.update_request(request.id_entity, request.employee, request.description, date2, request.status,
#                                   request.price)
#     if res:
#         return Response(status_code=status.HTTP_200_OK)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/update/customer")
# async def update_client(customer: datamodels.EditCustomer = Depends(datamodels.EditCustomer.as_form),
#                         user: datamodels.User = Depends(check_token)):
#     res = database.update_customer(customer.id_entity, customer.name, customer.phone_number, customer.email)
#     if res:
#         return Response(status_code=status.HTTP_200_OK)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.post("/update/employee")
# async def update_employee(employee: datamodels.EditEmployee = Depends(datamodels.EditEmployee.as_form),
#                           user: datamodels.User = Depends(check_token)):
#     res = database.update_employee(employee.id_entity, employee.email, employee.department, employee.activated,
#                                    employee.admin_permissions, employee.name, employee.phone_number)
#     if res:
#         return Response(status_code=status.HTTP_200_OK)
#     else:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#
#
# @app.get("/get/departments")
# async def get_departments(user: datamodels.User = Depends(check_token)):
#     res = database.get_departments()
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.get("/get/customers")
# async def get_customers(user: datamodels.User = Depends(check_token)):
#     res = database.get_customers()
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.get("/get/employees")
# async def get_employees(user: datamodels.User = Depends(check_token)):
#     res = database.get_employees_with_departs()
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# @app.post("/edit/employee")
# async def edit_employee(payload: datamodels.EditEmployee):
#     new_payload = {}
#
#
# @app.get("/get/requests_date")
# async def get_requests_date(scope=None, date_from1=None, date_to1=None, user: datamodels.User = Depends(check_token)):
#     date_from = datetime.now() - timedelta(days=30) if not date_from1 else datetime.strptime(date_from1, '%m/%d/%Y')
#     date_to = datetime.now() if not date_to1 else datetime.strptime(date_to1 + "_23:59", '%m/%d/%Y_%H:%M')
#     if datetime.timestamp(date_to) - datetime.timestamp(date_from) < 0:
#         return Response(status_code=status.HTTP_400_BAD_REQUEST)
#     res = database.get_requests_by_dates(date_from, date_to) if not scope else database.get_requests_by_date_and_employee(
#         date_from, date_to,
#         scope)
#     if not res:
#         return Response(status_code=status.HTTP_404_NOT_FOUND)
#     json_compatible_res = jsonable_encoder(res)
#     return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_res)
#
#
# asyncio.create_task(database.user_logout_task())
