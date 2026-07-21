from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status

from app.dependencies.classes import get_class_service
from app.dependencies.setting import get_setting_service
from app.dependencies.page_section import get_page_section_service
from app.dependencies.teachers import get_teacher_service
from app.responses.api_response import ApiResponse
from app.services.class_service import ClassService
from app.services.page_section_service import PageSectionService
from app.services.setting_service import SettingService
from app.services.teacher_service import TeacherService

router = APIRouter(prefix="/landing", tags=["Landing"])


@router.get("", response_model=ApiResponse[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_landing(
    setting_service: SettingService = Depends(get_setting_service),
    page_section_service: PageSectionService = Depends(get_page_section_service),
    teacher_service: TeacherService = Depends(get_teacher_service),
    class_service: ClassService = Depends(get_class_service),
):
    """Landing page aggregation endpoint."""
    settings_response = await setting_service.list_settings()
    sections_response = await page_section_service.list_sections()
    teachers_response = await teacher_service.list_teachers(page=1, limit=20)
    classes_response = await class_service.list_classes(page=1, limit=20)

    settings = [item.model_dump() for item in settings_response.data or []]
    sections = {item.section_type: item.model_dump() for item in sections_response.data or []}
    teachers = [item.model_dump() for item in teachers_response.data or []]
    classes = [item.model_dump() for item in classes_response.data or []]

    data = {
        "settings": settings,
        "sections": sections,
        "teachers": teachers,
        "classes": classes,
    }

    return ApiResponse(success=True, message="Success", data=data)
