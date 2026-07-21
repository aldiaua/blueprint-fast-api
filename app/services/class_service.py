from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import ProgrammingError

from app.config.logger import logger
from app.repositories.class_repository import ClassRepository
from app.responses.api_response import ApiResponse, PaginatedResponse, PaginationMeta
from app.schemas.classes import ClassCreate, ClassDetail, ClassItem, ClassUpdate


class ClassService:
    def __init__(self, repository: ClassRepository):
        self.repository = repository

    async def list_classes(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        year: Optional[int] = None,
    ) -> PaginatedResponse[ClassItem]:
        logger.info(
            "class_list_requested", page=page, limit=limit, search=search, year=year
        )

        try:
            total = await self.repository.count_active_classes(search=search, year=year)
            classes = await self.repository.find_active_classes(
                page=page,
                limit=limit,
                search=search,
                year=year,
            )
        except ProgrammingError as exc:
            logger.error("class_list_database_error", error=str(exc))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database schema is not ready: missing classes table or related database objects.",
            ) from exc

        data: List[ClassItem] = [
            ClassItem(
                uuid=str(item["uuid"]),
                name=item["name"],
                slug=item["slug"],
                description=item.get("description"),
                cover_image=item.get("cover_image"),
                graduation_year=item["graduation_year"],
            )
            for item in classes
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

    async def get_class_detail(self, uuid: str) -> ApiResponse[ClassDetail]:
        logger.info("class_detail_requested", uuid=uuid)

        try:
            class_record = await self.repository.find_active_class_by_uuid(uuid)
        except ProgrammingError as exc:
            logger.error("class_detail_database_error", error=str(exc), uuid=uuid)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database schema is not ready.",
            ) from exc

        if not class_record:
            logger.warning("class_not_found", uuid=uuid)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with uuid {uuid} not found.",
            )

        # Build homeroom teacher info if available
        homeroom_teacher = None
        if class_record.get("teacher_uuid"):
            homeroom_teacher = {
                "uuid": str(class_record["teacher_uuid"]),
                "name": class_record.get("teacher_name"),
                "position": class_record.get("teacher_position"),
            }

        return ApiResponse(
            success=True,
            message="Success",
            data=ClassDetail(
                uuid=str(class_record["uuid"]),
                name=class_record["name"],
                slug=class_record["slug"],
                description=class_record.get("description"),
                cover_image=class_record.get("cover_image"),
                graduation_year=class_record["graduation_year"],
                homeroom_teacher=homeroom_teacher,
            ),
        )

    async def list_classes_cms(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        year: Optional[int] = None,
        sort: str = "name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[ClassItem]:
        total = await self.repository.count_classes(
            search=search,
            year=year,
            is_active=is_active,
        )
        classes = await self.repository.find_classes(
            page=page,
            limit=limit,
            search=search,
            year=year,
            sort=sort,
            order=order,
            is_active=is_active,
        )

        data: List[ClassItem] = [
            ClassItem(
                uuid=str(item["uuid"]),
                name=item["name"],
                slug=item["slug"],
                description=item.get("description"),
                cover_image=item.get("cover_image"),
                graduation_year=item["graduation_year"],
            )
            for item in classes
        ]

        return PaginatedResponse(
            success=True,
            message="Success",
            data=data,
            meta=PaginationMeta(page=page, size=limit, total=total),
        )

    async def get_class_by_uuid(self, uuid: str) -> ApiResponse[ClassDetail]:
        class_record = await self.repository.find_class_by_uuid(uuid)

        if not class_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Class with uuid {uuid} not found.")

        homeroom_teacher = None
        if class_record.get("teacher_uuid"):
            homeroom_teacher = {
                "uuid": str(class_record["teacher_uuid"]),
                "name": class_record.get("teacher_name"),
                "position": class_record.get("teacher_position"),
            }

        return ApiResponse(
            success=True,
            message="Success",
            data=ClassDetail(
                uuid=str(class_record["uuid"]),
                name=class_record["name"],
                slug=class_record["slug"],
                description=class_record.get("description"),
                cover_image=class_record.get("cover_image"),
                graduation_year=class_record["graduation_year"],
                homeroom_teacher=homeroom_teacher,
            ),
        )

    async def create_class(self, class_payload: ClassCreate) -> ApiResponse[ClassDetail]:
        data = class_payload.model_dump()
        if data.get("homeroom_teacher_uuid"):
            data["homeroom_teacher_id"] = await self.repository.find_teacher_id_by_uuid(data["homeroom_teacher_uuid"])
        else:
            data["homeroom_teacher_id"] = None
        created = await self.repository.create_class(data)
        return ApiResponse(
            success=True,
            message="Success",
            data=ClassDetail(
                uuid=str(created["uuid"]),
                name=created["name"],
                slug=created["slug"],
                description=created.get("description"),
                cover_image=created.get("cover_image"),
                graduation_year=created["graduation_year"],
                homeroom_teacher=None,
            ),
        )

    async def update_class(self, uuid: str, class_payload: ClassUpdate) -> ApiResponse[ClassDetail]:
        data = class_payload.model_dump(exclude_unset=True)
        if data.get("homeroom_teacher_uuid"):
            data["homeroom_teacher_id"] = await self.repository.find_teacher_id_by_uuid(data["homeroom_teacher_uuid"])
        updated = await self.repository.update_class(uuid, data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
        return ApiResponse(
            success=True,
            message="Success",
            data=ClassDetail(
                uuid=str(updated["uuid"]),
                name=updated["name"],
                slug=updated["slug"],
                description=updated.get("description"),
                cover_image=updated.get("cover_image"),
                graduation_year=updated["graduation_year"],
                homeroom_teacher=None,
            ),
        )

    async def delete_class(self, uuid: str) -> ApiResponse[None]:
        existing = await self.repository.find_class_by_uuid(uuid)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
        await self.repository.delete_class(uuid)
        return ApiResponse(success=True, message="Success", data=None)
