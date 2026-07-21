from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.config.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse


class AuthService:
    """
    Service for handling authentication, including password hashing and JWT creation.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password: The plain text password.
            hashed_password: The hashed password from the database.

        Returns:
            True if the password is correct, False otherwise.
        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Hashes a plain text password.

        Args:
            password: The plain text password.

        Returns:
            The hashed password.
        """
        return cls.pwd_context.hash(password)

    @staticmethod
    def create_access_token(subject: Any, expires_delta: timedelta | None = None) -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def login(self, *, username: str, password: str) -> TokenResponse:
        """
        Authenticate a user and return a JWT token.
        """
        user = await self.user_repository.find_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        access_token = self.create_access_token(subject=user.uuid)
        return TokenResponse(access_token=access_token)