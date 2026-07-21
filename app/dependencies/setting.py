from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.setting_repository import SettingRepository
from app.services.setting_service import SettingService


async def get_setting_service(
    db_session: AsyncSession = Depends(get_db),
) -> SettingService:
    """Dependency injection for SettingService."""
    repository = SettingRepository(db=db_session)
    return SettingService(repository=repository)
