from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import User


class UserRepository:
    """
    Repository for user-related database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_by_username(self, username: str) -> User | None:
        """
        Find a user by their username.
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_user_by_uuid(self, user_uuid: str) -> User | None:
        """
        Find a user by their UUID.
        """
        stmt = select(User).where(User.uuid == user_uuid)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()