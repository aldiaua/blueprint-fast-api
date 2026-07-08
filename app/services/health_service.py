from fastapi import HTTPException, status

from app.config.logger import logger
from app.repositories.health_repository import HealthRepository
from app.responses.api_response import ApiResponse
from app.schemas.health import HealthResponse


class HealthService:
    def __init__(self, repository: HealthRepository):
        self.repository = repository

    async def check(self):
        logger.info("health_check_started")
        db_ok = await self.repository.check_database()
        logger.info(
            "health_check_finished",
            database=db_ok,
        )
        if not db_ok:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed sync database",
            )
        return ApiResponse(
            success=True,
            message="Health check success",
            data=HealthResponse(
                status="UP",
                database="UP" if db_ok else "DOWN",
            ),
        )
