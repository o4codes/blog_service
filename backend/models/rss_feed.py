from datetime import datetime
from bson import ObjectId
from models.utils.custom_type import PyObjectId
from pydantic import AnyUrl, BaseModel, EmailStr, Field


class RssFeed(BaseModel):
    """Model of RSS feeds
    """

    id: PyObjectId = Field(default_factory=PyObjectId)
    title: str
    link: AnyUrl
    description: str
    published_date: datetime 
    provider_id = Field(default_factory=PyObjectId)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
