from typing import Optional
from fastapi import HTTPException

from app.repositories.student_repository import StudentRepository
from app.responses.api_response import ApiResponse, PaginatedResponse, PaginationMeta
from app.schemas.student import StudentCreate, StudentDetail, StudentItem, StudentUpdate


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def list_students(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
    ) -> PaginatedResponse[StudentItem]:
        """List active students with pagination and optional filters."""
        try:
            total = await self.repository.count_active_students(
                search=search,
                class_uuid=class_uuid,
            )
            data = await self.repository.find_active_students(
                page=page,
                limit=limit,
                search=search,
                class_uuid=class_uuid,
            )

            students = [StudentItem(**row) for row in data]
            meta = PaginationMeta(page=page, size=limit, total=total)

            return PaginatedResponse(
                success=True,
                message="Success",
                data=students,
                meta=meta,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching students: {str(e)}",
            )

    async def get_student_detail(self, uuid: str) -> ApiResponse[StudentDetail]:
        """Get student detail by UUID."""
        try:
            data = await self.repository.find_active_student_by_uuid(uuid)

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found",
                )

            student = StudentDetail(**data)
            return ApiResponse(
                success=True,
                message="Success",
                data=student,
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching student: {str(e)}",
            )

    async def get_students_by_class(
        self,
        class_uuid: str,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> PaginatedResponse[StudentItem]:
        """Get students by class UUID with pagination."""
        try:
            data, total = await self.repository.find_students_by_class_uuid(
                class_uuid=class_uuid,
                page=page,
                limit=limit,
                search=search,
            )

            students = [StudentItem(**row) for row in data]
            meta = PaginationMeta(page=page, size=limit, total=total)

            return PaginatedResponse(
                success=True,
                message="Success",
                data=students,
                meta=meta,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching class students: {str(e)}",
            )

    async def list_students_cms(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
        sort: str = "full_name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[StudentItem]:
        try:
            total = await self.repository.count_students(
                search=search,
                class_uuid=class_uuid,
                is_active=is_active,
            )
            data = await self.repository.find_students(
                page=page,
                limit=limit,
                search=search,
                class_uuid=class_uuid,
                sort=sort,
                order=order,
                is_active=is_active,
            )

            students = [StudentItem(**row) for row in data]
            meta = PaginationMeta(page=page, size=limit, total=total)

            return PaginatedResponse(
                success=True,
                message="Success",
                data=students,
                meta=meta,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching students: {str(e)}",
            )

    async def get_student_by_uuid(self, uuid: str) -> ApiResponse[StudentDetail]:
        try:
            data = await self.repository.find_student_by_uuid(uuid)
            if not data:
                raise HTTPException(status_code=404, detail="Student not found")
            student = StudentDetail(**data)
            return ApiResponse(success=True, message="Success", data=student)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")

    async def create_student(self, student_payload: StudentCreate) -> ApiResponse[StudentDetail]:
        try:
            payload = student_payload.model_dump()
            class_id = await self.repository.find_class_id_by_uuid(payload.pop("class_uuid"))
            if class_id is None:
                raise HTTPException(status_code=404, detail="Class not found")
            payload["class_id"] = class_id
            created = await self.repository.create_student(payload)
            return ApiResponse(success=True, message="Success", data=StudentDetail(**created))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")

    async def update_student(self, uuid: str, student_payload: StudentUpdate) -> ApiResponse[StudentDetail]:
        try:
            payload = student_payload.model_dump(exclude_unset=True)
            if class_uuid := payload.pop("class_uuid", None):
                class_id = await self.repository.find_class_id_by_uuid(class_uuid)
                if class_id is None:
                    raise HTTPException(status_code=404, detail="Class not found")
                payload["class_id"] = class_id
            updated = await self.repository.update_student(uuid, payload)
            if not updated:
                raise HTTPException(status_code=404, detail="Student not found")
            return ApiResponse(success=True, message="Success", data=StudentDetail(**updated))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")

    async def delete_student(self, uuid: str) -> ApiResponse[None]:
        try:
            existing = await self.repository.find_student_by_uuid(uuid)
            if not existing:
                raise HTTPException(status_code=404, detail="Student not found")
            await self.repository.delete_student(uuid)
            return ApiResponse(success=True, message="Success", data=None)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")
