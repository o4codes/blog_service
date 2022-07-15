from typing import List
from fastapi import BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from requests import head

from core.dependencies import get_database
from application.schema.subscriber import (
    SubscriberRequestSchema,
    SubscriberResponseSchema,
)
from models.subscriber import Subscriber
from services.subscriber import SubscriberService
from services.auth import AuthService
from services.utils.mailing import Mailing, TemplateBodyVars

router = APIRouter(prefix="/subscribers", tags=["SUBSCRIBER"])


@router.get("/", response_model=List[SubscriberResponseSchema])
async def get_all_subscribers(database: str = Depends(get_database)):
    """Get all subscribers"""
    return await SubscriberService(database).list()


@router.get("/{id}", response_model=SubscriberResponseSchema)
async def get_subscriber(id: str, database: str = Depends(get_database)):
    """Get subscriber by id"""
    subscriber = await SubscriberService(database).get_by_id(id)
    return SubscriberResponseSchema(**subscriber.dict())


@router.post(
    "/", response_model=SubscriberResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_subscriber(
    background_tasks: BackgroundTasks,
    subscriber: SubscriberRequestSchema, 
    database: str = Depends(get_database),
    
):
    """Create subscriber"""
    subscriber = Subscriber(**subscriber.dict())
    subscriber_created: Subscriber = await SubscriberService(database).create(
        subscriber
    )
    
    # send activation mail to subscriber
    token_url = await AuthService(database).create_token_url(
        "api/v1/auth/activate", subscriber_created
    )
    mailing = Mailing()
    template_vars = TemplateBodyVars(
        header="Activate your account",
        body=f"To complete your registration, please click on the link below:",
        action=token_url,
        action_message="Activate Account",
    )
    background_tasks.add_task(
        mailing.send_email, 
        "Complete Registeration", 
        template_vars, 
        subscriber_created.email 
    )
    return SubscriberResponseSchema(**subscriber_created.dict())


@router.put("/{id}", response_model=SubscriberResponseSchema)
async def update_subscriber(
    id: str, subscriber: SubscriberRequestSchema, database: str = Depends(get_database)
):
    """Update subscriber"""
    return await SubscriberService(database).update(id, subscriber)


@router.delete("/{id}", response_class=JSONResponse)
async def delete_subscriber(id: str, database: str = Depends(get_database)):
    """Delete subscriber"""
    await SubscriberService(database).delete(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Subscriber deleted"}
    )
