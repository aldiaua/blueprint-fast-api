from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.teacher_repository import TeacherRepository
from app.services.teacher_service import TeacherService


def get_teacher_service(
    db: AsyncSession = Depends(get_db),
) -> TeacherService:
    repository = TeacherRepository(db)
    return TeacherService(repository)
