from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.classes import get_class_service
from app.dependencies.page_section import get_page_section_service
from app.dependencies.setting import get_setting_service
from app.dependencies.student import get_student_service
from app.dependencies.teachers import get_teacher_service
from app.responses.api_response import ApiResponse, PaginatedResponse
from app.schemas.classes import ClassCreate, ClassDetail, ClassItem, ClassUpdate
from app.schemas.page_section import (
    PageSectionDetail,
    PageSectionItem,
    PageSectionUpdate,
)
from app.schemas.setting import SettingDetail, SettingItem, SettingUpdate
from app.schemas.student import StudentCreate, StudentDetail, StudentItem, StudentUpdate
from app.schemas.teacher import TeacherCreate, TeacherDetail, TeacherItem, TeacherUpdate
from app.services.class_service import ClassService
from app.services.page_section_service import PageSectionService
from app.services.setting_service import SettingService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService

# Main CMS Router (memerlukan auth untuk operasi CRUD)
router = APIRouter(prefix="/cms", tags=["CMS"], dependencies=[Depends(get_current_active_user)])


# Settings
@router.get(
    "/settings",
    response_model=ApiResponse[list[SettingItem]],
    status_code=status.HTTP_200_OK,
)
async def cms_list_settings(
    setting_service: SettingService = Depends(get_setting_service),
):
    return await setting_service.list_settings()


@router.get(
    "/settings/{setting_key}",
    response_model=ApiResponse[SettingDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_get_setting_detail(
    setting_key: str,
    setting_service: SettingService = Depends(get_setting_service),
):
    return await setting_service.get_setting_detail(setting_key)


@router.put(
    "/settings/{setting_key}",
    response_model=ApiResponse[SettingDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_update_setting(
    setting_key: str,
    payload: SettingUpdate,
    setting_service: SettingService = Depends(get_setting_service),
):
    return await setting_service.update_setting(setting_key, payload)


# Page Sections
@router.get(
    "/page-sections",
    response_model=ApiResponse[list[PageSectionItem]],
    status_code=status.HTTP_200_OK,
)
async def cms_list_page_sections(
    page_section_service: PageSectionService = Depends(get_page_section_service),
):
    return await page_section_service.list_sections()


@router.get(
    "/page-sections/{section_type}",
    response_model=ApiResponse[PageSectionDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_get_page_section_detail(
    section_type: str,
    page_section_service: PageSectionService = Depends(get_page_section_service),
):
    return await page_section_service.get_section_detail(section_type)


@router.put(
    "/page-sections/{section_type}",
    response_model=ApiResponse[PageSectionDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_update_page_section(
    section_type: str,
    payload: PageSectionUpdate,
    page_section_service: PageSectionService = Depends(get_page_section_service),
):
    return await page_section_service.update_section(section_type, payload)


# Teachers
@router.get(
    "/teachers",
    response_model=PaginatedResponse[TeacherItem],
    status_code=status.HTTP_200_OK,
)
async def cms_list_teachers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    sort: str = Query("name"),
    order: str = Query("asc"),
    is_active: Optional[bool] = Query(None),
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.list_teachers_cms(
        page=page,
        limit=limit,
        search=search,
        sort=sort,
        order=order,
        is_active=is_active,
    )


@router.get(
    "/teachers/{uuid}",
    response_model=ApiResponse[TeacherDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_get_teacher_detail(
    uuid: str,
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.get_teacher_by_uuid(uuid)


@router.post(
    "/teachers",
    response_model=ApiResponse[TeacherDetail],
    status_code=status.HTTP_201_CREATED,
)
async def cms_create_teacher(
    payload: TeacherCreate,
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.create_teacher(payload)


@router.put(
    "/teachers/{uuid}",
    response_model=ApiResponse[TeacherDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_update_teacher(
    uuid: str,
    payload: TeacherUpdate,
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.update_teacher(uuid, payload)


@router.delete(
    "/teachers/{uuid}",
    response_model=ApiResponse[Any],
    status_code=status.HTTP_200_OK,
)
async def cms_delete_teacher(
    uuid: str,
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.delete_teacher(uuid)


# Classes
@router.get(
    "/classes",
    response_model=PaginatedResponse[ClassItem],
    status_code=status.HTTP_200_OK,
)
async def cms_list_classes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    sort: str = Query("name"),
    order: str = Query("asc"),
    is_active: Optional[bool] = Query(None),
    service: ClassService = Depends(get_class_service),
):
    return await service.list_classes_cms(
        page=page,
        limit=limit,
        search=search,
        year=year,
        sort=sort,
        order=order,
        is_active=is_active,
    )


@router.get(
    "/classes/{uuid}",
    response_model=ApiResponse[ClassDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_get_class_detail(
    uuid: str,
    service: ClassService = Depends(get_class_service),
):
    return await service.get_class_by_uuid(uuid)


@router.post(
    "/classes",
    response_model=ApiResponse[ClassDetail],
    status_code=status.HTTP_201_CREATED,
)
async def cms_create_class(
    payload: ClassCreate,
    service: ClassService = Depends(get_class_service),
):
    return await service.create_class(payload)


@router.put(
    "/classes/{uuid}",
    response_model=ApiResponse[ClassDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_update_class(
    uuid: str,
    payload: ClassUpdate,
    service: ClassService = Depends(get_class_service),
):
    return await service.update_class(uuid, payload)


@router.delete(
    "/classes/{uuid}",
    response_model=ApiResponse[Any],
    status_code=status.HTTP_200_OK,
)
async def cms_delete_class(
    uuid: str,
    service: ClassService = Depends(get_class_service),
):
    return await service.delete_class(uuid)


# Students
@router.get(
    "/students",
    response_model=PaginatedResponse[StudentItem],
    status_code=status.HTTP_200_OK,
)
async def cms_list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    class_uuid: Optional[str] = Query(None),
    sort: str = Query("full_name"),
    order: str = Query("asc"),
    is_active: Optional[bool] = Query(None),
    service: StudentService = Depends(get_student_service),
):
    return await service.list_students_cms(
        page=page,
        limit=limit,
        search=search,
        class_uuid=class_uuid,
        sort=sort,
        order=order,
        is_active=is_active,
    )


@router.get(
    "/students/{uuid}",
    response_model=ApiResponse[StudentDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_get_student_detail(
    uuid: str,
    service: StudentService = Depends(get_student_service),
):
    return await service.get_student_by_uuid(uuid)


@router.post(
    "/students",
    response_model=ApiResponse[StudentDetail],
    status_code=status.HTTP_201_CREATED,
)
async def cms_create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.create_student(payload)


@router.put(
    "/students/{uuid}",
    response_model=ApiResponse[StudentDetail],
    status_code=status.HTTP_200_OK,
)
async def cms_update_student(
    uuid: str,
    payload: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    return await service.update_student(uuid, payload)


@router.delete(
    "/students/{uuid}",
    response_model=ApiResponse[Any],
    status_code=status.HTTP_200_OK,
)
async def cms_delete_student(
    uuid: str,
    service: StudentService = Depends(get_student_service),
):
    return await service.delete_student(uuid)
