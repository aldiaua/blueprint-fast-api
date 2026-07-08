from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    # Connection Pool
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    # Development
    echo=settings.APP_DEBUG,
    # Future SQLAlchemy
    future=True,
    # Connection Health Check
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
