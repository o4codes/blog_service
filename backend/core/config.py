import secrets

from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = config("DEBUG", cast=bool, default=True)
    SWAGGER_URL: str = API_V1_STR + "/docs"
    REDOC_URL: str = API_V1_STR + "/redoc"

    DATABASE_URL: str = config(
        "DATABASE_URL", cast=str, default="mongodb://localhost:27017"
    )
    DATABASE_NAME: str = "o4codes-blog"
    SUBSCRIBER_COLLECTION: str = "subscribers"
    RSS_PROVIDER_COLLECTION: str = "rss_providers"

    PROJECT_NAME: str = "o4codes-blog-API"
    PROJECT_DESCRIPTION: str = "o4codes blog API"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_AUTHOR: str = "o4codes"
    PROJECT_AUTHOR_EMAIL: str = "o4codes@outlook.com"


settings = Settings()
