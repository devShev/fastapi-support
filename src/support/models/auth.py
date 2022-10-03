from enum import Enum

from pydantic import BaseModel


class UserGroup(str, Enum):
    USER = 'user'
    MODER = 'moder'


class BaseUser(BaseModel):
    email: str
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    user_group: UserGroup

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
