from fastapi import APIRouter, Depends, Query, status

from app.dependencies.classes import get_class_service
from app.dependencies.student import get_student_service
from app.responses.api_response import ApiResponse, PaginatedResponse
from app.schemas.classes import ClassDetail, ClassItem
from app.schemas.student import StudentItem
from app.services.class_service import ClassService
from app.services.student_service import StudentService

router = APIRouter()


@router.get(
    "/classes",
    response_model=PaginatedResponse[ClassItem],
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
)
async def get_classes(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search by class name"),
    year: int | None = Query(None, description="Filter by graduation year"),
    service: ClassService = Depends(get_class_service),
):
    return await service.list_classes(page=page, limit=limit, search=search, year=year)


@router.get(
    "/classes/{uuid}",
    response_model=ApiResponse[ClassDetail],
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
)
async def get_class_detail(
    uuid: str,
    service: ClassService = Depends(get_class_service),
):
    return await service.get_class_detail(uuid)


@router.get(
    "/classes/{class_uuid}/students",
    response_model=PaginatedResponse[StudentItem],
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
)
async def get_students_by_class(
    class_uuid: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search by student name"),
    student_service: StudentService = Depends(get_student_service),
):
    return await student_service.get_students_by_class(
        class_uuid=class_uuid,
        page=page,
        limit=limit,
        search=search,
    )
