import pydantic


from pydantic import BaseModel, EmailStr

class SubscriberCreateModel(BaseModel):
    email: EmailStr