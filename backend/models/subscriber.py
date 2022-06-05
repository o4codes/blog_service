from bson import ObjectId
from models.utils.custom_type import PyObjectId
from pydantic import BaseModel, EmailStr, Field


class Subscriber(BaseModel):
    """Model to rerprenet subscriber of the blog"""

    id: PyObjectId = Field(default_factory=PyObjectId)
    email: EmailStr

    class Config:
        """Config for pydantic to handle json serialization"""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
