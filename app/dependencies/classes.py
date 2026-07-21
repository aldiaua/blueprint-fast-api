from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.class_repository import ClassRepository
from app.services.class_service import ClassService


def get_class_service(
    db: AsyncSession = Depends(get_db),
) -> ClassService:
    repository = ClassRepository(db)
    return ClassService(repository)
