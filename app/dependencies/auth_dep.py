from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AuthService:
    """Dependency injection for AuthService."""
    user_repo = UserRepository(db)
    return AuthService(user_repo)