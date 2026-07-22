from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from app.context.request_context import request_id_ctx

T = TypeVar("T")


# 1. Standar Response Tunggal (Satu Objek atau Dict)
class ApiResponse(BaseModel, Generic[T]):
    request_id: str | None = Field(
        default_factory=request_id_ctx.get
    )
    success: bool
    message: str
    data: Optional[T] = None


# 2. Metadata untuk Pagination
class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int


# 3. Standar Response untuk Data List/Array Berhalaman
class PaginatedResponse(BaseModel, Generic[T]):
    request_id: str | None = Field(
        default_factory=request_id_ctx.get
    )
    success: bool
    message: str
    data: List[T] = []
    meta: PaginationMeta
