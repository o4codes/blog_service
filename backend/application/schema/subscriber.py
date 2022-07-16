from pydantic import BaseModel
from bson import ObjectId
from models.utils.custom_type import PyObjectId
from models.subscriber import Subscriber


class SubscriberRequestSchema(BaseModel):
    email: str
    name: str
    password: str


class SubscriberResponseSchema(BaseModel):
    id: PyObjectId
    email: str
    name: str
    subscribed_blogs: list
    created_at: str

    class Config:
        """Config for pydantic to handle json serialization"""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class LoginResponseSchema(BaseModel):
    id: PyObjectId
    email: str
    name: str
    access_token: str
    token_type: str

    class Config:
        """Config for pydantic to handle json serialization"""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
