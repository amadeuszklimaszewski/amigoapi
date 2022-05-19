import datetime as dt
from uuid import UUID
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    birthday: dt.date


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(UserBaseSchema):
    password: str
    password2: str


class UserUpdateInputSchema(BaseModel):
    first_name: str
    last_name: str
    birthday: dt.date


class UserOutputSchema(UserBaseSchema):
    id: UUID
    is_active: bool

    class Config:
        orm_mode = True
