from typing import Optional, List
from fastapi import HTTPException

from app.repositories.setting_repository import SettingRepository
from app.responses.api_response import ApiResponse
from app.schemas.setting import SettingDetail, SettingItem, SettingUpdate


class SettingService:
    def __init__(self, repository: SettingRepository):
        self.repository = repository

    async def list_settings(self) -> ApiResponse[List[SettingItem]]:
        """List all settings."""
        try:
            data = await self.repository.find_all_settings()
            settings = [SettingItem(**row) for row in data]

            return ApiResponse(
                success=True,
                message="Success",
                data=settings,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching settings: {str(e)}",
            )

    async def get_setting_detail(self, setting_key: str) -> ApiResponse[SettingDetail]:
        """Get setting detail by key."""
        try:
            data = await self.repository.find_setting_by_key(setting_key)

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Setting '{setting_key}' not found",
                )

            setting = SettingDetail(**data)
            return ApiResponse(
                success=True,
                message="Success",
                data=setting,
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching setting: {str(e)}",
            )

    async def update_setting(self, setting_key: str, setting_payload: SettingUpdate) -> ApiResponse[SettingDetail]:
        try:
            data = setting_payload.model_dump(exclude_unset=True)
            updated = await self.repository.update_setting(
                setting_key=setting_key,
                components=data.get("components"),
                styles=data.get("styles"),
            )
            if not updated:
                raise HTTPException(status_code=404, detail=f"Setting '{setting_key}' not found")
            return ApiResponse(success=True, message="Success", data=SettingDetail(**updated))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating setting: {str(e)}")
