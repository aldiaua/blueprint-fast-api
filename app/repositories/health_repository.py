from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_database(self) -> bool:
        try:
            await self.db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
