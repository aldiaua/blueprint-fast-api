from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class TeacherRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_active_teachers(self, search: Optional[str] = None) -> int:
        query = "SELECT COUNT(1) FROM teachers WHERE is_active = TRUE"
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND (name ILIKE :search OR position ILIKE :search OR subject ILIKE :search)"
            parameters["search"] = f"%{search}%"

        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_active_teachers(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, position, subject, photo "
            "FROM teachers "
            "WHERE is_active = TRUE"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND (name ILIKE :search OR position ILIKE :search OR subject ILIKE :search)"
            parameters["search"] = f"%{search}%"

        query += " ORDER BY sort_order ASC, name ASC LIMIT :limit OFFSET :offset"

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_active_teacher_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, position, subject, quote, biography, photo, "
            "email, phone, instagram, linkedin "
            "FROM teachers "
            "WHERE uuid = :uuid AND is_active = TRUE"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def count_teachers(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        sort: str = "name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> int:
        query = "SELECT COUNT(1) FROM teachers WHERE 1=1"
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND (name ILIKE :search OR position ILIKE :search OR subject ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if is_active is not None:
            query += " AND is_active = :is_active"
            parameters["is_active"] = is_active

        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_teachers(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        sort: str = "name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, position, subject, quote, biography, photo, "
            "email, phone, instagram, linkedin, sort_order, is_active "
            "FROM teachers WHERE 1=1"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND (name ILIKE :search OR position ILIKE :search OR subject ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if is_active is not None:
            query += " AND is_active = :is_active"
            parameters["is_active"] = is_active

        sort_column = (
            sort if sort in {"name", "position", "subject", "sort_order"} else "name"
        )
        sort_direction = "ASC" if order.lower() == "asc" else "DESC"
        query += f" ORDER BY {sort_column} {sort_direction}, name ASC LIMIT :limit OFFSET :offset"

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_teacher_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT uuid, name, position, subject, quote, biography, photo, "
            "email, phone, instagram, linkedin, sort_order, is_active "
            "FROM teachers WHERE uuid = :uuid"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def create_teacher(self, teacher_data: Dict[str, Any]) -> Dict[str, Any]:
        query = (
            "INSERT INTO teachers (uuid, name, position, subject, quote, biography, photo, "
            "email, phone, instagram, linkedin, sort_order, is_active, created_at, updated_at) "
            "VALUES (uuid_generate_v4(), :name, :position, :subject, :quote, :biography, :photo, "
            ":email, :phone, :instagram, :linkedin, :sort_order, :is_active, NOW(), NOW()) "
            "RETURNING uuid, name, position, subject, quote, biography, photo, email, phone, instagram, linkedin, sort_order, is_active"
        )
        result = await self.db.execute(text(query), teacher_data)
        await self.db.commit()
        return dict(result.mappings().first())

    async def update_teacher(
        self, uuid: str, teacher_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        query = (
            "UPDATE teachers SET "
            "name = COALESCE(:name, name), "
            "position = COALESCE(:position, position), "
            "subject = COALESCE(:subject, subject), "
            "quote = COALESCE(:quote, quote), "
            "biography = COALESCE(:biography, biography), "
            "photo = COALESCE(:photo, photo), "
            "email = COALESCE(:email, email), "
            "phone = COALESCE(:phone, phone), "
            "instagram = COALESCE(:instagram, instagram), "
            "linkedin = COALESCE(:linkedin, linkedin), "
            "sort_order = COALESCE(:sort_order, sort_order), "
            "is_active = COALESCE(:is_active, is_active), "
            "updated_at = NOW() "
            "WHERE uuid = :uuid "
            "RETURNING uuid, name, position, subject, quote, biography, photo, email, phone, instagram, linkedin, sort_order, is_active"
        )
        parameters = {**teacher_data, "uuid": uuid}
        result = await self.db.execute(text(query), parameters)
        await self.db.commit()
        row = result.mappings().first()
        return dict(row) if row else None

    async def delete_teacher(self, uuid: str) -> bool:
        query = "DELETE FROM teachers WHERE uuid = :uuid"
        await self.db.execute(text(query), {"uuid": uuid})
        await self.db.commit()
        return True
