from typing import List
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import AnyUrl

from models.rss_provider import RssProvider
from core.dependencies import get_database, get_current_user, get_admin_user
from services.rss_provider import RssProviderService

router = APIRouter(prefix="/rss_providers", tags=["RSS_PROVIDER"])


@router.get("/", response_model=List[RssProvider])
async def list_rss_providers(
    db=Depends(get_database),
    current_user=Depends(get_current_user),
    ):
    """Gets a list of all rss providers"""
    rss_provider_service = RssProviderService(db)
    rss_providers = await rss_provider_service.list()
    return rss_providers


@router.get("/{id}", response_model=RssProvider)
async def get_rss_provider_by_id(
    id: str, 
    db=Depends(get_database),
    current_user=Depends(get_current_user),
    ):
    """Gets a rss provider by id"""
    rss_provider_service = RssProviderService(db)
    rss_provider = await rss_provider_service.get_by_id(id)
    return rss_provider


@router.post("/", response_model=RssProvider, status_code=status.HTTP_201_CREATED)
async def create_rss_provider(
    url: AnyUrl, 
    db=Depends(get_database),
    current_user=Depends(get_admin_user),
    ):
    """Creates a rss provider"""
    rss_provider_service = RssProviderService(db)
    rss_provider = await rss_provider_service.create(url)
    return rss_provider


@router.put("/{id}", response_model=RssProvider)
async def update_rss_provider(
    id: str, 
    url: AnyUrl, 
    db=Depends(get_database),
    current_user=Depends(get_admin_user),
    ):
    """Updates a rss provider"""
    rss_provider_service = RssProviderService(db)
    rss_provider = await rss_provider_service.update(id, url)
    return rss_provider


@router.delete("/{id}", response_class=JSONResponse)
async def delete_rss_provider(
    id: str, 
    db=Depends(get_database),
    current_user=Depends(get_admin_user),
    ):
    """Deletes a rss provider"""
    await RssProviderService(db).delete(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Rss provider deleted"}
    )
