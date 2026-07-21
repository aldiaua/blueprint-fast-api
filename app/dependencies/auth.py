from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.config.security import ALGORITHM, SECRET_KEY
from app.models.base import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Decodes the JWT token, validates it, and returns the current user.
    Raises HTTPException if the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid: str | None = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_uuid)
    except JWTError:
        raise credentials_exception from None

    user_repo = UserRepository(db)
    user = await user_repo.find_user_by_uuid(user_uuid=token_data.sub)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Checks if the current user is active.
    Raises HTTPException if the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user