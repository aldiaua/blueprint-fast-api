from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PageSectionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_active_sections(self) -> List[Dict[str, Any]]:
        query = (
            "SELECT section_type, title, components, styles, uuid, sort_order, is_active "
            "FROM page_sections "
            "WHERE is_active = TRUE "
            "ORDER BY sort_order ASC"
        )
        result = await self.db.execute(text(query))
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_section_by_type(self, section_type: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT section_type, title, components, styles, uuid, sort_order, is_active "
            "FROM page_sections "
            "WHERE section_type = :section_type AND is_active = TRUE"
        )
        result = await self.db.execute(text(query), {"section_type": section_type})
        row = result.mappings().first()
        return dict(row) if row else None

    async def update_section(self, section_type: str, components: Optional[Dict[str, Any]] = None, styles: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        query = (
            "UPDATE page_sections SET "
            "components = COALESCE(:components, components), "
            "styles = COALESCE(:styles, styles), "
            "updated_at = NOW() "
            "WHERE section_type = :section_type "
            "RETURNING section_type, title, components, styles, uuid, sort_order, is_active"
        )
        result = await self.db.execute(text(query), {"section_type": section_type, "components": components, "styles": styles})
        await self.db.commit()
        row = result.mappings().first()
        return dict(row) if row else None
