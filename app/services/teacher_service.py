from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import ProgrammingError

from app.config.logger import logger
from app.repositories.teacher_repository import TeacherRepository
from app.responses.api_response import ApiResponse, PaginatedResponse, PaginationMeta
from app.schemas.teacher import TeacherCreate, TeacherDetail, TeacherItem, TeacherUpdate


class TeacherService:
    def __init__(self, repository: TeacherRepository):
        self.repository = repository

    async def list_teachers(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> PaginatedResponse[TeacherItem]:
        logger.info("teacher_list_requested", page=page, limit=limit, search=search)

        try:
            total = await self.repository.count_active_teachers(search=search)
            teachers = await self.repository.find_active_teachers(
                page=page,
                limit=limit,
                search=search,
            )
        except ProgrammingError as exc:
            logger.error("teacher_list_database_error", error=str(exc))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database schema is not ready: missing teachers table or related database objects.",
            ) from exc

        data: List[TeacherItem] = [
            TeacherItem(
                uuid=str(item["uuid"]),
                name=item["name"],
                position=item["position"],
                subject=item.get("subject"),
                photo=item.get("photo"),
            )
            for item in teachers
        ]

        return PaginatedResponse(
            success=True,
            message="Success",
            data=data,
            meta=PaginationMeta(
                page=page,
                size=limit,
                total=total,
            ),
        )

    async def get_teacher_detail(self, uuid: str) -> ApiResponse[TeacherDetail]:
        logger.info("teacher_detail_requested", uuid=uuid)

        try:
            teacher = await self.repository.find_active_teacher_by_uuid(uuid)
        except ProgrammingError as exc:
            logger.error("teacher_detail_database_error", error=str(exc), uuid=uuid)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database schema is not ready.",
            ) from exc

        if not teacher:
            logger.warning("teacher_not_found", uuid=uuid)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with uuid {uuid} not found.",
            )

        return ApiResponse(
            success=True,
            message="Success",
            data=TeacherDetail(
                uuid=str(teacher["uuid"]),
                name=teacher["name"],
                position=teacher["position"],
                subject=teacher.get("subject"),
                photo=teacher.get("photo"),
                quote=teacher.get("quote"),
                biography=teacher.get("biography"),
                email=teacher.get("email"),
                phone=teacher.get("phone"),
                instagram=teacher.get("instagram"),
                linkedin=teacher.get("linkedin"),
            ),
        )

    async def list_teachers_cms(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        sort: str = "name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[TeacherItem]:
        logger.info(
            "teacher_cms_list_requested",
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            order=order,
            is_active=is_active,
        )

        total = await self.repository.count_teachers(
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            order=order,
            is_active=is_active,
        )
        teachers = await self.repository.find_teachers(
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            order=order,
            is_active=is_active,
        )

        data: List[TeacherItem] = [
            TeacherItem(
                uuid=str(item["uuid"]),
                name=item["name"],
                position=item["position"],
                subject=item.get("subject"),
                photo=item.get("photo"),
            )
            for item in teachers
        ]

        return PaginatedResponse(
            success=True,
            message="Success",
            data=data,
            meta=PaginationMeta(page=page, size=limit, total=total),
        )

    async def get_teacher_by_uuid(self, uuid: str) -> ApiResponse[TeacherDetail]:
        teacher = await self.repository.find_teacher_by_uuid(uuid)

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )

        return ApiResponse(
            success=True,
            message="Success",
            data=TeacherDetail(
                uuid=str(teacher["uuid"]),
                name=teacher["name"],
                position=teacher["position"],
                subject=teacher.get("subject"),
                photo=teacher.get("photo"),
                quote=teacher.get("quote"),
                biography=teacher.get("biography"),
                email=teacher.get("email"),
                phone=teacher.get("phone"),
                instagram=teacher.get("instagram"),
                linkedin=teacher.get("linkedin"),
            ),
        )

    async def create_teacher(
        self, teacher: TeacherCreate
    ) -> ApiResponse[TeacherDetail]:
        teacher_data = teacher.model_dump()
        created = await self.repository.create_teacher(teacher_data)
        if created is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Internal Server Error",
            )
        return ApiResponse(
            success=True,
            message="Success",
            data=TeacherDetail(
                uuid=str(created["uuid"]),
                name=created["name"],
                position=created["position"],
                subject=created.get("subject"),
                photo=created.get("photo"),
                quote=created.get("quote"),
                biography=created.get("biography"),
                email=created.get("email"),
                phone=created.get("phone"),
                instagram=created.get("instagram"),
                linkedin=created.get("linkedin"),
            ),
        )

    async def update_teacher(
        self, uuid: str, teacher: TeacherUpdate
    ) -> ApiResponse[TeacherDetail]:
        teacher_data = teacher.model_dump(exclude_unset=True)
        updated = await self.repository.update_teacher(uuid, teacher_data)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )

        return ApiResponse(
            success=True,
            message="Success",
            data=TeacherDetail(
                uuid=str(updated["uuid"]),
                name=updated["name"],
                position=updated["position"],
                subject=updated.get("subject"),
                photo=updated.get("photo"),
                quote=updated.get("quote"),
                biography=updated.get("biography"),
                email=updated.get("email"),
                phone=updated.get("phone"),
                instagram=updated.get("instagram"),
                linkedin=updated.get("linkedin"),
            ),
        )

    async def delete_teacher(self, uuid: str) -> ApiResponse[None]:
        existing = await self.repository.find_teacher_by_uuid(uuid)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )
        await self.repository.delete_teacher(uuid)
        return ApiResponse(success=True, message="Success", data=None)
