from datetime import datetime
from decimal import Decimal
from fastapi import Form
from pydantic import BaseModel


class NewCustomer(BaseModel):
    name: str
    phone_number: str
    email: str | None = None

    @classmethod
    def as_form(cls, name=Form(...), phone_number=Form(...), email=Form(...)) -> 'NewCustomer':
        return cls(name=name, phone_number=phone_number, email=email)


class NewRequest(BaseModel):
    id_customer: int
    id_employee: int
    item: str
    description: str

    @classmethod
    def as_form(cls, id_customer=Form(...), id_employee=Form(...), item=Form(...), description=Form(...)) -> 'NewRequest':
        return cls(id_customer=id_customer, id_employee=id_employee, item=item, description=description)


class NewEmployee(BaseModel):
    username: str
    password: str
    name: str | None = None
    email: str
    phone_number: str
    department_id: int
    activated: bool | None = None
    admin_permissions: bool | None = None

    @classmethod
    def as_form(cls, username=Form(...), email=Form(...), password=Form(...), department_id=Form(...), activated=Form(...), name=Form(...), phone_number=Form(...)) -> 'NewEmployee':
        return cls(username=username, email=email, password=password, department_id=department_id, activated=activated, name=name, phone_number=phone_number)


class NewDepartment(BaseModel):
    name: str

    @classmethod
    def as_form(cls, name=Form(...)) -> 'NewDepartment':
        return cls(name=name)


class EditCustomer(BaseModel):
    id_entity: int
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None

    @classmethod
    def as_form(cls, id_entity=Form(...), name=Form(...), phone_number=Form(...), email=Form(...)) -> 'EditCustomer':
        return cls(id_entity=id_entity, name=name, phone_number=phone_number, email=email)


class EditRequest(BaseModel):
    id_entity: int
    employee: int | None = None
    description: str | None = None
    status: int | None = None
    price: Decimal | None = None

    @classmethod
    def as_form(cls, id_entity=Form(...), employee=Form(...), description=Form(...), status=Form(...), price=Form(...)) -> 'EditRequest':
        return cls(id_entity=id_entity, employee=employee, description=description, status=status, price=price)


class EditEmployee(BaseModel):
    id_entity: int
    username: str | None = None
    email: str | None = None
    department: int | None = None
    activated: bool | None = None
    admin_permissions: bool | None = None
    name: str | None = None
    phone_number: str | None = None

    @classmethod
    def as_form(cls, id_entity=Form(...), username=Form(...), email=Form(...), password=Form(...), department=Form(...), activated=Form(...), admin_permissions=Form(...), name=Form(...), phone_number=Form(...)) -> 'EditEmployee':
        return cls(id_entity=id_entity, username=username, email=email, password=password, department=department, activated=activated, admin_permissions=admin_permissions, name=name, phone_number=phone_number)
