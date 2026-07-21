from typing import Optional

from pydantic import BaseModel, Field


class ClassItem(BaseModel):
    uuid: str
    name: str
    slug: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    graduation_year: int


class ClassDetail(BaseModel):
    uuid: str
    name: str
    slug: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    graduation_year: int
    homeroom_teacher: Optional[dict] = None  # Simple teacher info if available


class ClassQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None
    year: Optional[int] = None


class ClassCreate(BaseModel):
    name: str
    slug: str
    graduation_year: int
    sort_order: Optional[int] = Field(default=0, ge=0)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    homeroom_teacher_uuid: Optional[str] = None
    is_active: Optional[bool] = True


class ClassUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    graduation_year: Optional[int] = None
    sort_order: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    homeroom_teacher_uuid: Optional[str] = None
    is_active: Optional[bool] = None
