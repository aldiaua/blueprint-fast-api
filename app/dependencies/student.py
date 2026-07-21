from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.student_repository import StudentRepository
from app.services.student_service import StudentService


async def get_student_service(
    db_session: AsyncSession = Depends(get_db),
) -> StudentService:
    """Dependency injection for StudentService."""
    repository = StudentRepository(db=db_session)
    return StudentService(repository=repository)
