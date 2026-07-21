from typing import List
from fastapi import HTTPException

from app.repositories.page_section_repository import PageSectionRepository
from app.responses.api_response import ApiResponse
from app.schemas.page_section import PageSectionDetail, PageSectionItem, PageSectionUpdate


class PageSectionService:
    def __init__(self, repository: PageSectionRepository):
        self.repository = repository

    async def list_sections(self) -> ApiResponse[List[PageSectionItem]]:
        try:
            data = await self.repository.find_active_sections()
            sections = [PageSectionItem(**row) for row in data]
            return ApiResponse(success=True, message="Success", data=sections)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching page sections: {str(e)}")

    async def get_section_detail(self, section_type: str) -> ApiResponse[PageSectionDetail]:
        try:
            data = await self.repository.find_section_by_type(section_type)
            if not data:
                raise HTTPException(status_code=404, detail="Section not found")
            section = PageSectionDetail(**data)
            return ApiResponse(success=True, message="Success", data=section)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching page section: {str(e)}")

    async def update_section(self, section_type: str, section_payload: PageSectionUpdate) -> ApiResponse[PageSectionDetail]:
        try:
            data = section_payload.model_dump(exclude_unset=True)
            updated = await self.repository.update_section(
                section_type=section_type,
                components=data.get("components"),
                styles=data.get("styles"),
            )
            if not updated:
                raise HTTPException(status_code=404, detail="Section not found")
            return ApiResponse(success=True, message="Success", data=PageSectionDetail(**updated))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating page section: {str(e)}")
