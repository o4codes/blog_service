import motor.motor_asyncio
from core.config import settings


def get_database():
    """Retrieves database connection object"""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    return client[settings.DATABASE_NAME]
