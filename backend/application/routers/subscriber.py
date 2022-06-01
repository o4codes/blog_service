from typing import List
from fastapi import Body, Depends, status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from core.dependencies import get_database
from core.exception_handler import AppExceptionHandler
from services.subscriber import SubscriberService
from models.subscriber import Subscriber

router = APIRouter(prefix="/subscribers", tags=["SUBSCRIBER"])

@router.get("/", response_model=List[Subscriber])
async def get_all_subscribers(database: str = Depends(get_database)):
    """ Get all subscribers
    """
    try:
        return await SubscriberService(database).list()
    except Exception as e:
        AppExceptionHandler(e).raiseException()


@router.get("/{id}", response_model=Subscriber)
async def get_subscriber(id: str, database: str = Depends(get_database)):
    """ Get subscriber by id
    """
    try:
        return await SubscriberService(database).get_by_id(id)
    except Exception as e:
        AppExceptionHandler(e).raiseException()

@router.post("/", response_model=Subscriber, status_code=status.HTTP_201_CREATED)
async def create_subscriber(email: EmailStr = Body(...), database: str = Depends(get_database)):
    """ Create subscriber
    """
    try:
        return await SubscriberService(database).create(email)
    except Exception as e:
        AppExceptionHandler(e).raiseException()


@router.put("/{id}", response_model=Subscriber)
async def update_subscriber(
    id: str, 
    subscriber: Subscriber, 
    database: str = Depends(get_database)
    ):
    """ Update subscriber
    """
    try:
        return await SubscriberService(database).update(id, subscriber)
    except Exception as e:
        AppExceptionHandler(e).raiseException()

@router.delete("/{id}", response_class=JSONResponse)
async def delete_subscriber(id: str, database: str = Depends(get_database)):
    """ Delete subscriber
    """
    try:
        await SubscriberService(database).delete(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Subscriber deleted"})

    except Exception as e:
        AppExceptionHandler(e).raiseException()