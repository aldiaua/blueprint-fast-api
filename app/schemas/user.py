from typing import Optional
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=127)
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserDetail(BaseModel):
    uuid: str
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str = "admin"
    is_active: bool = True
