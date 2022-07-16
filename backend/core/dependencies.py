import motor.motor_asyncio
from fastapi.security import HTTPBearer
from fastapi import Depends

from core.exceptions import NotFoundException, UnauthorizedException
from core.config import settings
from services.auth import AuthService

token_auth_scheme = HTTPBearer()

def get_database():
    """Retrieves database connection object"""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    return client[settings.DATABASE_NAME]


async def get_current_user(token: HTTPBearer = Depends(token_auth_scheme)):
    """Retrieves current user from token"""
    print(token)
    auth_service = AuthService(get_database())
    try:
        subscriber = await auth_service.get_subscriber_by_token(token.credentials)
        return subscriber
    except NotFoundException:
        raise UnauthorizedException("Invalid authentication credentials")
