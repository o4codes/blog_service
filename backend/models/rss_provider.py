from bson import ObjectId
from models.utils.custom_type import PyObjectId
from pydantic import AnyUrl, BaseModel, EmailStr, Field


class RssProvider(BaseModel):
    """Model of RSS providers"""

    id: PyObjectId = Field(default_factory=PyObjectId)
    url: AnyUrl
    title: str
    description: str
    image: AnyUrl

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
