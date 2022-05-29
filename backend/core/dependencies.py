import motor.motor_asyncio
from .config import settings

def get_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    return client[settings.DATABASE_NAME]