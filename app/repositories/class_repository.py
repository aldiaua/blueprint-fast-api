from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class ClassRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_active_classes(
        self, search: Optional[str] = None, year: Optional[int] = None
    ) -> int:
        query = "SELECT COUNT(1) FROM classes WHERE is_active = TRUE"
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND name ILIKE :search"
            parameters["search"] = f"%{search}%"

        if year:
            query += " AND graduation_year = :year"
            parameters["year"] = year

        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_active_classes(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, slug, description, cover_image, graduation_year "
            "FROM classes "
            "WHERE is_active = TRUE"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND name ILIKE :search"
            parameters["search"] = f"%{search}%"

        if year:
            query += " AND graduation_year = :year"
            parameters["year"] = year

        query += " ORDER BY sort_order ASC, name ASC LIMIT :limit OFFSET :offset"

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_active_class_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT c.uuid, c.name, c.slug, c.description, c.cover_image, c.graduation_year, "
            "t.uuid AS teacher_uuid, t.name AS teacher_name, t.position AS teacher_position "
            "FROM classes c "
            "LEFT JOIN teachers t ON c.homeroom_teacher_id = t.id "
            "WHERE c.uuid = :uuid AND c.is_active = TRUE"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def find_classes(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        year: Optional[int] = None,
        sort: str = "name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, slug, description, cover_image, graduation_year, "
            "sort_order, is_active, homeroom_teacher_id "
            "FROM classes WHERE 1=1"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND name ILIKE :search"
            parameters["search"] = f"%{search}%"

        if year:
            query += " AND graduation_year = :year"
            parameters["year"] = year

        if is_active is not None:
            query += " AND is_active = :is_active"
            parameters["is_active"] = is_active

        sort_column = (
            sort if sort in {"name", "graduation_year", "sort_order"} else "name"
        )
        sort_direction = "ASC" if order.lower() == "asc" else "DESC"
        query += f" ORDER BY {sort_column} {sort_direction}, name ASC LIMIT :limit OFFSET :offset"

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def count_classes(
        self,
        search: Optional[str] = None,
        year: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        query = "SELECT COUNT(1) FROM classes WHERE 1=1"
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND name ILIKE :search"
            parameters["search"] = f"%{search}%"

        if year:
            query += " AND graduation_year = :year"
            parameters["year"] = year

        if is_active is not None:
            query += " AND is_active = :is_active"
            parameters["is_active"] = is_active

        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_class_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT c.uuid, c.name, c.slug, c.description, c.cover_image, c.graduation_year, "
            "c.sort_order, c.is_active, c.homeroom_teacher_id, t.uuid AS teacher_uuid, "
            "t.name AS teacher_name, t.position AS teacher_position "
            "FROM classes c "
            "LEFT JOIN teachers t ON c.homeroom_teacher_id = t.id "
            "WHERE c.uuid = :uuid"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def find_teacher_id_by_uuid(self, uuid: str) -> Optional[int]:
        query = "SELECT id FROM teachers WHERE uuid = :uuid"
        result = await self.db.execute(text(query), {"uuid": uuid})
        return result.scalar_one_or_none()

    async def create_class(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        query = (
            "INSERT INTO classes (uuid, name, slug, description, cover_image, homeroom_teacher_id, "
            "graduation_year, sort_order, is_active, created_at, updated_at) "
            "VALUES (uuid_generate_v4(), :name, :slug, :description, :cover_image, :homeroom_teacher_id, "
            ":graduation_year, :sort_order, :is_active, NOW(), NOW()) "
            "RETURNING uuid, name, slug, description, cover_image, graduation_year, sort_order, is_active, homeroom_teacher_id"
        )
        result = await self.db.execute(text(query), class_data)
        await self.db.commit()
        return dict(result.mappings().first())

    async def update_class(
        self, uuid: str, class_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        query = (
            "UPDATE classes SET "
            "name = COALESCE(:name, name), "
            "slug = COALESCE(:slug, slug), "
            "description = COALESCE(:description, description), "
            "cover_image = COALESCE(:cover_image, cover_image), "
            "homeroom_teacher_id = COALESCE(:homeroom_teacher_id, homeroom_teacher_id), "
            "graduation_year = COALESCE(:graduation_year, graduation_year), "
            "sort_order = COALESCE(:sort_order, sort_order), "
            "is_active = COALESCE(:is_active, is_active), "
            "updated_at = NOW() "
            "WHERE uuid = :uuid "
            "RETURNING uuid, name, slug, description, cover_image, graduation_year, sort_order, is_active, homeroom_teacher_id"
        )
        parameters = {**class_data, "uuid": uuid}
        result = await self.db.execute(text(query), parameters)
        await self.db.commit()
        row = result.mappings().first()
        return dict(row) if row else None

    async def delete_class(self, uuid: str) -> bool:
        query = "DELETE FROM classes WHERE uuid = :uuid"
        await self.db.execute(text(query), {"uuid": uuid})
        await self.db.commit()
        return True
