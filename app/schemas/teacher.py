from typing import Optional

from pydantic import BaseModel, Field


class TeacherItem(BaseModel):
    uuid: str
    name: str
    position: str
    subject: Optional[str] = None
    photo: Optional[str] = None


class TeacherDetail(BaseModel):
    uuid: str
    name: str
    position: str
    subject: Optional[str] = None
    photo: Optional[str] = None
    quote: Optional[str] = None
    biography: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None


class TeacherQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None


class TeacherCreate(BaseModel):
    name: str
    position: str
    subject: Optional[str] = None
    quote: Optional[str] = None
    biography: Optional[str] = None
    photo: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    sort_order: Optional[int] = Field(default=0, ge=0)
    is_active: Optional[bool] = True


class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    subject: Optional[str] = None
    quote: Optional[str] = None
    biography: Optional[str] = None
    photo: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    sort_order: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None
