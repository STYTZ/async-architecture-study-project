from pydantic import BaseModel

import models


class SignUp(BaseModel):
    login: str
    password: str
    email: str


class Login(BaseModel):
    login: str
    password: str


class UserCreatedEvent(BaseModel):
    public_id: str
    login: str
    email: str
    role: models.Role
