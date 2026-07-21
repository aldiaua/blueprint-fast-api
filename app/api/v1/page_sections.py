from typing import List
from fastapi import APIRouter, Depends, status

from app.dependencies.page_section import get_page_section_service
from app.responses.api_response import ApiResponse
from app.schemas.page_section import PageSectionDetail, PageSectionItem
from app.services.page_section_service import PageSectionService

router = APIRouter(prefix="/page-sections", tags=["PageSections"])


@router.get(
    "",
    response_model=ApiResponse[List[PageSectionItem]],
    status_code=status.HTTP_200_OK,
)
async def list_page_sections(
    page_section_service: PageSectionService = Depends(get_page_section_service),
):
    """List active page sections for the public website."""
    return await page_section_service.list_sections()


@router.get(
    "/{section_type}",
    response_model=ApiResponse[PageSectionDetail],
    status_code=status.HTTP_200_OK,
)
async def get_page_section_detail(
    section_type: str,
    page_section_service: PageSectionService = Depends(get_page_section_service),
):
    """Get active page section by type."""
    return await page_section_service.get_section_detail(section_type)
