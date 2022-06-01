from typing import List
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from pydantic import AnyUrl

from core.dependencies import get_database
from core.exception_handler import AppExceptionHandler
from services.rss_provider import RssProviderService
from models.rss_provider import RssProvider


router = APIRouter(prefix = "/rss_providers", tags = ["RSS_PROVIDER"])

@router.get("/", response_model = List[RssProvider])
async def list_rss_providers( db: AppExceptionHandler = Depends(get_database)):
    """ Gets a list of all rss providers 
    """
    rss_provider_service = RssProviderService(db)
    rss_providers = await rss_provider_service.list()
    return rss_providers


@router.get("/{id}", response_model = RssProvider)
async def get_rss_provider_by_id(id: str, db: AppExceptionHandler = Depends(get_database)):
    """ Gets a rss provider by id
    """
    try:
        rss_provider_service = RssProviderService(db)
        rss_provider = await rss_provider_service.get_by_id(id)
        return rss_provider
    except Exception as e:
        AppExceptionHandler.raiseException(e)


@router.post("/", response_model = RssProvider, status_code = status.HTTP_201_CREATED)
async def create_rss_provider(
    url: AnyUrl, 
    db: AppExceptionHandler = Depends(get_database)
    ):
    """ Creates a rss provider
    """
    try:
        rss_provider_service = RssProviderService(db)
        rss_provider = await rss_provider_service.create(url)
        return rss_provider
    except Exception as e:
        print(e)
        AppExceptionHandler.raiseException(e)


@router.put("/{id}", response_model = RssProvider)
async def update_rss_provider(
    id: str, 
    url: AnyUrl,
    db: AppExceptionHandler = Depends(get_database)
    ):
    """ Updates a rss provider
    """
    try:
        rss_provider_service = RssProviderService(db)
        rss_provider = await rss_provider_service.update(id, url)
        return rss_provider
    except Exception as e:
        AppExceptionHandler.raiseException(e)


@router.delete("/{id}", response_class = JSONResponse)
async def delete_rss_provider(id: str, db: AppExceptionHandler = Depends(get_database)):
    """ Deletes a rss provider
    """
    try:
        await RssProviderService(db).delete(id)
        return JSONResponse(status_code = status.HTTP_200_OK, content = {"message": "Rss provider deleted"})
    except Exception as e:
        AppExceptionHandler.raiseException(e)

    
