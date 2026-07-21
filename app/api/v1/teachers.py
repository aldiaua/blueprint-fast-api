from fastapi import APIRouter, Depends, Query, status

from app.dependencies.teachers import get_teacher_service
from app.responses.api_response import PaginatedResponse, ApiResponse
from app.schemas.teacher import TeacherItem, TeacherDetail
from app.services.teacher_service import TeacherService

router = APIRouter()


@router.get(
    "/teachers",
    response_model=PaginatedResponse[TeacherItem],
    status_code=status.HTTP_200_OK,
    tags=["Teachers"],
)
async def get_teachers(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search by name, position, or subject"),
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.list_teachers(page=page, limit=limit, search=search)


@router.get(
    "/teachers/{uuid}",
    response_model=ApiResponse[TeacherDetail],
    status_code=status.HTTP_200_OK,
    tags=["Teachers"],
)
async def get_teacher_detail(
    uuid: str,
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.get_teacher_detail(uuid)
