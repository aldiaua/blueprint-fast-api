from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SettingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all_settings(self) -> List[Dict[str, Any]]:
        """Find all settings."""
        query = (
            "SELECT setting_key, components, styles "
            "FROM settings "
            "ORDER BY setting_key ASC"
        )
        result = await self.db.execute(text(query))
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def find_setting_by_key(self, setting_key: str) -> Optional[Dict[str, Any]]:
        """Find a single setting by key."""
        query = (
            "SELECT setting_key, components, styles, description "
            "FROM settings "
            "WHERE setting_key = :setting_key"
        )
        result = await self.db.execute(text(query), {"setting_key": setting_key})
        row = result.mappings().first()
        return dict(row) if row else None

    async def update_setting(self, setting_key: str, components: Optional[Dict[str, Any]] = None, styles: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        query = (
            "UPDATE settings SET "
            "components = COALESCE(:components, components), "
            "styles = COALESCE(:styles, styles), "
            "updated_at = NOW() "
            "WHERE setting_key = :setting_key "
            "RETURNING setting_key, components, styles, description"
        )
        result = await self.db.execute(text(query), {"setting_key": setting_key, "components": components, "styles": styles})
        await self.db.commit()
        row = result.mappings().first()
        return dict(row) if row else None
