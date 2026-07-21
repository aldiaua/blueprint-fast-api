from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Blueprint Service"
    APP_DEBUG: bool = True

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT Secret Key
    SECRET_KEY: str

    # Storage Configuration for local uploads
    LOCAL_STORAGE_PATH: str = "uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()  # type: ignore
