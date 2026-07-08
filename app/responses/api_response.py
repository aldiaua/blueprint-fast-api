from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None


class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int


class PaginatedResponse(ApiResponse[T], Generic[T]):
    meta: PaginationMeta
