import datetime
from typing import Any

import pydantic



class Role(pydantic.BaseModel):
    name: str
    id: str
    created_on: datetime.datetime
    created_by: str


class UserRole(pydantic.BaseModel):
    added_by: str
    added_on: datetime.datetime
    role: Role


class User(pydantic.BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: int
    role: UserRole
    is_email_confirmed: bool
    is_phone_confirmed: bool
    updated_by: int | None
    updated_on: datetime.datetime


class Authentication(pydantic.BaseModel):
    access_token: str
    token_type: str