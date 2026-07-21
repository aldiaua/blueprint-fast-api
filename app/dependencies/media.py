from app.services.media_service import MediaService


def get_media_service() -> MediaService:
    """Dependency for MediaService."""
    return MediaService()