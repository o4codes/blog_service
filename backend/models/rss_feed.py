from typing import List
from datetime import datetime
from bson import ObjectId
from models.utils.custom_type import PyObjectId
from pydantic import AnyUrl, BaseModel, Field

class ViewerDescription(BaseModel):
    datetime: datetime 
    viewer_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RssFeed(BaseModel):
    """Model of RSS feeds"""

    id: PyObjectId = Field(default_factory=PyObjectId)
    title: str
    link: AnyUrl
    description: str
    published_date: datetime
    provider_id: PyObjectId = Field(default_factory=PyObjectId)
    viewers: List[ViewerDescription] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
