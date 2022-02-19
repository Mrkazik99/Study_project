import datetime

from pydantic import BaseModel


class NewCustomer(BaseModel):
    name: str
    phone_number: str
    email: str | None = None


class NewRequest(BaseModel):
    id_employee: int
    id_customer: int
    item: str
    description: str
    status: int
    date0: datetime.datetime
    date1: datetime.datetime
    price: float | None = None


class NewEmployee(BaseModel):
    username: str
    email: str
    password: str
    department_id: int
    activated: bool | None = None
    name: str | None = None
    phone_number: str


class NewDepartment(BaseModel):
    name: str


class EditCustomer(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None


class EditRequest(BaseModel):
    id_employee: int | None = None
    id_customer: int | None = None
    item: str | None = None
    description: str | None = None
    status: int | None = None
    date0: datetime.datetime | None = None
    date1: datetime.datetime | None = None
    date2: datetime.datetime | None = None
    price: float | None = None


class EditEmployee(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    department_id: int | None = None
    activated: bool | None = None
    name: str | None = None
    phone_number: str | None = None


class EditDepartment(BaseModel):
    name: str | None = None
