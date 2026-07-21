from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class SettingItem(BaseModel):
    """Setting item for list responses."""
    
    setting_key: str = Field(..., description="Unique setting key (enum: website, header, footer, seo, social, theme)")
    components: Dict[str, Any] = Field(default_factory=dict, description="Components configuration")
    styles: Dict[str, Any] = Field(default_factory=dict, description="Styles configuration")

    class Config:
        from_attributes = True


class SettingUpdate(BaseModel):
    components: Optional[Dict[str, Any]] = None
    styles: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class SettingDetail(BaseModel):
    """Setting detail response."""
    
    setting_key: str = Field(..., description="Unique setting key")
    components: Dict[str, Any] = Field(default_factory=dict, description="Components configuration")
    styles: Dict[str, Any] = Field(default_factory=dict, description="Styles configuration")
    description: Optional[str] = Field(None, description="Setting description")

    class Config:
        from_attributes = True
