from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.media import get_media_service
from app.models.base import User
from app.responses.api_response import ApiResponse
from app.services.media_service import MediaService

router = APIRouter(
    prefix="/cms/media",
    tags=["CMS Media"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post(
    "/upload",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_media(
    file: UploadFile = File(...),
    media_service: MediaService = Depends(get_media_service),
    # This line ensures the endpoint is protected
    _: User = Depends(get_current_active_user),
):
    """Uploads a media file (image, pdf) to the server."""
    file_data = await media_service.save_file(file=file, sub_folder="images")
    return ApiResponse(success=True, message="File uploaded successfully", data=file_data)