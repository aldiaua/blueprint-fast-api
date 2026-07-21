from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Schema for the response after a successful login.
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Schema for the data encoded within the JWT.
    """
    sub: str | None = None