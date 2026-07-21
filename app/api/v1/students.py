from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.student import get_student_service
from app.responses.api_response import ApiResponse, PaginatedResponse
from app.schemas.student import StudentDetail, StudentItem
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get(
    "",
    response_model=PaginatedResponse[StudentItem],
    status_code=status.HTTP_200_OK,
)
async def list_students(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or nickname"),
    class_uuid: Optional[str] = Query(None, description="Filter by class UUID"),
    student_service: StudentService = Depends(get_student_service),
):
    """List all active students with pagination and optional filters.
    
    Query Parameters:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - search: Search by full_name or nick_name (ILIKE)
    - class_uuid: Filter by class UUID
    """
    return await student_service.list_students(
        page=page,
        limit=limit,
        search=search,
        class_uuid=class_uuid,
    )


@router.get(
    "/{student_uuid}",
    response_model=ApiResponse[StudentDetail],
    status_code=status.HTTP_200_OK,
)
async def get_student_detail(
    student_uuid: UUID,
    student_service: StudentService = Depends(get_student_service),
):
    """Get student detail by UUID."""
    return await student_service.get_student_detail(str(student_uuid))


@router.get(
    "/class/{class_uuid}/students",
    response_model=PaginatedResponse[StudentItem],
    status_code=status.HTTP_200_OK,
)
async def get_students_by_class(
    class_uuid: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or nickname"),
    student_service: StudentService = Depends(get_student_service),
):
    """Get students for a specific class with pagination.
    
    Query Parameters:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - search: Search by full_name or nick_name (ILIKE)
    """
    return await student_service.get_students_by_class(
        class_uuid=str(class_uuid),
        page=page,
        limit=limit,
        search=search,
    )
