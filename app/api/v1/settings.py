from typing import List
from fastapi import APIRouter, Depends, status

from app.dependencies.setting import get_setting_service
from app.responses.api_response import ApiResponse
from app.schemas.setting import SettingDetail, SettingItem
from app.services.setting_service import SettingService

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get(
    "",
    response_model=ApiResponse[List[SettingItem]],
    status_code=status.HTTP_200_OK,
)
async def list_settings(
    setting_service: SettingService = Depends(get_setting_service),
):
    """List all website settings.
    
    Returns all available settings including website info, header, footer, SEO, social media, and theme configurations.
    """
    return await setting_service.list_settings()


@router.get(
    "/{setting_key}",
    response_model=ApiResponse[SettingDetail],
    status_code=status.HTTP_200_OK,
)
async def get_setting_detail(
    setting_key: str,
    setting_service: SettingService = Depends(get_setting_service),
):
    """Get specific setting by key.
    
    Setting keys: website, header, footer, seo, social, theme
    """
    return await setting_service.get_setting_detail(setting_key)
