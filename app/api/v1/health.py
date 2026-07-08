from fastapi import APIRouter, Depends, status

from app.dependencies.health import get_health_service
from app.responses.api_response import ApiResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get("/health", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def health(
    service: HealthService = Depends(get_health_service),
):
    return await service.check()
