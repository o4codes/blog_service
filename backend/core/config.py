import secrets

from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY")
    AUTH_EXP_TIME: int = config("AUTH_EXP_TIME", cast=int, default=15)
    DEBUG: bool = config("DEBUG", cast=bool, default=True)
    SWAGGER_URL: str = API_V1_STR + "/docs"
    REDOC_URL: str = API_V1_STR + "/redoc"

    FRONTEND_URL: str = config("FRONTEND_URL", default="http://localhost:8001")
    DATABASE_URL: str = config(
        "DATABASE_URL", cast=str, default="mongodb://localhost:27017"
    )
    DATABASE_NAME: str = "rss-feeders"
    SUBSCRIBER_COLLECTION: str = "subscribers"
    RSS_PROVIDER_COLLECTION: str = "rss_providers"
    RSS_FEEDS_COLLECTION: str = "rss_feeds"

    PROJECT_NAME: str = "rss-feed-api"
    PROJECT_DESCRIPTION: str = "api for getting rss feeds from providers"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_AUTHOR: str = "o4codes"
    PROJECT_AUTHOR_EMAIL: str = "o4codes@outlook.com"

    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = '2525'
    MAIL_FROM='o4codes@outlook.com'
    MAIL_FROM_NAME='dev@rss-fidder'


settings = Settings()
