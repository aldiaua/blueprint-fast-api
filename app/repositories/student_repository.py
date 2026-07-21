from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_active_students(
        self,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
    ) -> int:
        """Count active students with optional filters."""
        query = (
            "SELECT COUNT(1) FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE s.is_active = TRUE AND c.is_active = TRUE"
        )
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if class_uuid:
            query += " AND c.uuid = :class_uuid"
            parameters["class_uuid"] = class_uuid

        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_active_students(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Find active students with pagination and filters."""
        query = (
            "SELECT s.uuid, s.full_name, s.nick_name, s.photo, s.quote "
            "FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE s.is_active = TRUE AND c.is_active = TRUE"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if class_uuid:
            query += " AND c.uuid = :class_uuid"
            parameters["class_uuid"] = class_uuid

        query += (
            " ORDER BY s.sort_order ASC, s.full_name ASC LIMIT :limit OFFSET :offset"
        )

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_active_student_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Find a single student by UUID with class info."""
        query = (
            "SELECT s.uuid, s.class_id, s.nis, s.full_name, s.nick_name, s.gender, "
            "s.birth_place, s.birth_date, s.address, s.hobby, s.ambition, s.quote, "
            "s.photo, s.cover_image, s.instagram, s.tiktok, s.email, s.phone, "
            "s.sort_order, s.created_at, s.updated_at "
            "FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE s.uuid = :uuid AND s.is_active = TRUE AND c.is_active = TRUE"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def find_students_by_class_uuid(
        self,
        class_uuid: str,
        page: int,
        limit: int,
        search: Optional[str] = None,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Find students by class UUID with pagination."""
        count_query = (
            "SELECT COUNT(1) FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE c.uuid = :class_uuid AND s.is_active = TRUE AND c.is_active = TRUE"
        )
        parameters: Dict[str, Any] = {"class_uuid": class_uuid}

        if search:
            count_query += (
                " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"
            )
            parameters["search"] = f"%{search}%"

        result = await self.db.execute(text(count_query), parameters)
        total = int(result.scalar_one())

        query = (
            "SELECT s.uuid, s.full_name, s.nick_name, s.photo, s.quote "
            "FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE c.uuid = :class_uuid AND s.is_active = TRUE AND c.is_active = TRUE"
        )

        if search:
            query += " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"

        query += (
            " ORDER BY s.sort_order ASC, s.full_name ASC LIMIT :limit OFFSET :offset"
        )
        parameters["limit"] = limit
        parameters["offset"] = (page - 1) * limit

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        data = [dict(row) for row in rows]

        return data, total

    async def count_students(
        self,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        query = (
            "SELECT COUNT(1) FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE 1=1"
        )
        parameters: Dict[str, Any] = {}

        if search:
            query += " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if class_uuid:
            query += " AND c.uuid = :class_uuid"
            parameters["class_uuid"] = class_uuid

        if is_active is not None:
            query += " AND s.is_active = :is_active"
            parameters["is_active"] = is_active

        query += " AND c.is_active = TRUE"
        result = await self.db.execute(text(query), parameters)
        return int(result.scalar_one())

    async def find_students(
        self,
        page: int,
        limit: int,
        search: Optional[str] = None,
        class_uuid: Optional[str] = None,
        sort: str = "full_name",
        order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        query = (
            "SELECT s.uuid, s.full_name, s.nick_name, s.photo, s.quote, s.is_active, "
            "s.sort_order, c.uuid AS class_uuid "
            "FROM students s "
            "JOIN classes c ON s.class_id = c.id "
            "WHERE c.is_active = TRUE"
        )
        parameters: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
        }

        if search:
            query += " AND (s.full_name ILIKE :search OR s.nick_name ILIKE :search)"
            parameters["search"] = f"%{search}%"

        if class_uuid:
            query += " AND c.uuid = :class_uuid"
            parameters["class_uuid"] = class_uuid

        if is_active is not None:
            query += " AND s.is_active = :is_active"
            parameters["is_active"] = is_active

        sort_column = (
            sort if sort in {"full_name", "nick_name", "sort_order"} else "full_name"
        )
        sort_direction = "ASC" if order.lower() == "asc" else "DESC"
        query += f" ORDER BY {sort_column} {sort_direction} LIMIT :limit OFFSET :offset"

        result = await self.db.execute(text(query), parameters)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_student_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT s.uuid, s.class_id, s.nis, s.full_name, s.nick_name, s.gender, "
            "s.birth_place, s.birth_date, s.address, s.hobby, s.ambition, s.quote, "
            "s.photo, s.cover_image, s.instagram, s.tiktok, s.email, s.phone, "
            "s.sort_order, s.is_active, s.created_at, s.updated_at "
            "FROM students s "
            "WHERE s.uuid = :uuid"
        )
        result = await self.db.execute(text(query), {"uuid": uuid})
        row = result.mappings().first()
        return dict(row) if row else None

    async def find_class_id_by_uuid(self, class_uuid: str) -> Optional[int]:
        query = "SELECT id FROM classes WHERE uuid = :class_uuid"
        result = await self.db.execute(text(query), {"class_uuid": class_uuid})
        return result.scalar_one_or_none()

    async def create_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        query = (
            "INSERT INTO students (uuid, class_id, nis, full_name, nick_name, gender, birth_place, birth_date, "
            "address, hobby, ambition, quote, photo, cover_image, instagram, tiktok, email, phone, sort_order, is_active, created_at, updated_at) "
            "VALUES (uuid_generate_v4(), :class_id, :nis, :full_name, :nick_name, :gender, :birth_place, :birth_date, "
            ":address, :hobby, :ambition, :quote, :photo, :cover_image, :instagram, :tiktok, :email, :phone, :sort_order, :is_active, NOW(), NOW()) "
            "RETURNING uuid, class_id, nis, full_name, nick_name, gender, birth_place, birth_date, address, hobby, ambition, quote, "
            "photo, cover_image, instagram, tiktok, email, phone, sort_order, is_active, created_at, updated_at"
        )
        result = await self.db.execute(text(query), student_data)
        await self.db.commit()
        return dict(result.mappings().first())

    async def update_student(
        self, uuid: str, student_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        query = (
            "UPDATE students SET "
            "class_id = COALESCE(:class_id, class_id), "
            "nis = COALESCE(:nis, nis), "
            "full_name = COALESCE(:full_name, full_name), "
            "nick_name = COALESCE(:nick_name, nick_name), "
            "gender = COALESCE(:gender, gender), "
            "birth_place = COALESCE(:birth_place, birth_place), "
            "birth_date = COALESCE(:birth_date, birth_date), "
            "address = COALESCE(:address, address), "
            "hobby = COALESCE(:hobby, hobby), "
            "ambition = COALESCE(:ambition, ambition), "
            "quote = COALESCE(:quote, quote), "
            "photo = COALESCE(:photo, photo), "
            "cover_image = COALESCE(:cover_image, cover_image), "
            "instagram = COALESCE(:instagram, instagram), "
            "tiktok = COALESCE(:tiktok, tiktok), "
            "email = COALESCE(:email, email), "
            "phone = COALESCE(:phone, phone), "
            "sort_order = COALESCE(:sort_order, sort_order), "
            "is_active = COALESCE(:is_active, is_active), "
            "updated_at = NOW() "
            "WHERE uuid = :uuid "
            "RETURNING uuid, class_id, nis, full_name, nick_name, gender, birth_place, birth_date, address, hobby, ambition, quote, "
            "photo, cover_image, instagram, tiktok, email, phone, sort_order, is_active, created_at, updated_at"
        )
        parameters = {**student_data, "uuid": uuid}
        result = await self.db.execute(text(query), parameters)
        await self.db.commit()
        row = result.mappings().first()
        return dict(row) if row else None

    async def delete_student(self, uuid: str) -> bool:
        query = "DELETE FROM students WHERE uuid = :uuid"
        await self.db.execute(text(query), {"uuid": uuid})
        await self.db.commit()
        return True
