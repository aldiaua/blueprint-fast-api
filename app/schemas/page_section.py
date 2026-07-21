from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PageSectionItem(BaseModel):
    section_type: str = Field(..., description="Section type")
    title: str = Field(..., description="Section title")
    components: Dict[str, Any] = Field(default_factory=dict, description="Section content")
    styles: Dict[str, Any] = Field(default_factory=dict, description="Section style configuration")

    class Config:
        from_attributes = True


class PageSectionUpdate(BaseModel):
    components: Optional[Dict[str, Any]] = None
    styles: Optional[Dict[str, Any]] = None


class PageSectionDetail(PageSectionItem):
    uuid: UUID = Field(..., description="Section UUID")
    sort_order: int = Field(..., description="Section display order")
    is_active: bool = Field(..., description="Section publish status")
