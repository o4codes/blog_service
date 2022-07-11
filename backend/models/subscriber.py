from bson import ObjectId
from models.utils.custom_type import PyObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

from models.utils.custom_type import PyObjectId


class Subscriber(BaseModel):
    """Model to rerprenet subscriber of the blog"""

    id: PyObjectId = Field(default_factory=PyObjectId)
    name: str
    email: EmailStr
    is_verified: bool = False
    subscribed_blogs: List[PyObjectId] = Field(default_factory=list)
    password: str
    created_at: str = datetime.now().isoformat()

    class Config:
        """Config for pydantic to handle json serialization"""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
