from app.config.settings import settings

# JWT Configuration
# To generate a good secret key, run: openssl rand -hex 32
# The secret key is now managed centrally in the Settings class
SECRET_KEY = settings.SECRET_KEY

# Algorithm for signing the JWT
ALGORITHM = "HS256"

# Access token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day