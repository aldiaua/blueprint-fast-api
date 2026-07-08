from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.health_repository import HealthRepository
from app.services.health_service import HealthService


def get_health_service(
    db: AsyncSession = Depends(get_db),
) -> HealthService:
    repository = HealthRepository(db)
    return HealthService(repository)
