import datetime as dt
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=5)
    email: EmailStr
    first_name: str
    last_name: str
    birthday: dt.date


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(UserBaseSchema):
    password: str = Field(..., min_length=8)
    password2: str = Field(..., min_length=8)


class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserOutputSchema(UserBaseSchema):
    id: UUID
    is_active: bool

    class Config:
        orm_mode = True
