from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.page_section_repository import PageSectionRepository
from app.services.page_section_service import PageSectionService


async def get_page_section_service(
    db_session: AsyncSession = Depends(get_db),
) -> PageSectionService:
    repository = PageSectionRepository(db=db_session)
    return PageSectionService(repository=repository)
