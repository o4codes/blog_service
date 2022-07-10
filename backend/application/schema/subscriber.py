from pydantic import BaseModel
from models.subscriber import Subscriber

class SubscriberRequestSchema(BaseModel):
    email: str
    name: str
    password: str

class SubscriberResponseSchema(BaseModel):
    id: str
    email: str
    name: str
    subscribed_blogs: list
    created_at: str