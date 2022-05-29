from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from models.utils.custom_type import PyObjectId

class Subscriber(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    email: EmailStr

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}