"""Authentication endpoints for user login."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth_dep import get_auth_service
from app.schemas.auth import TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user with username and password to obtain access token.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Login endpoint for user authentication.

    Args:
        form_data: User login credentials (username and password from a form).
        auth_service: Injected authentication service.

    Returns:
        TokenResponse containing the access token.

    Raises:
        HTTPException: If credentials are invalid or user is inactive.
    """
    try:
        token_response = await auth_service.login(
            username=form_data.username,
            password=form_data.password,
        )
        return token_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        ) from e
