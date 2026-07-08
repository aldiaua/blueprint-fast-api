from fastapi import APIRouter, Depends

from app.dependencies.health import get_health_service
from app.responses.api_response import ApiResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get("/health", response_model=ApiResponse)
async def health(
    service: HealthService = Depends(get_health_service),
):
    return await service.check()
