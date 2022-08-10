import asyncio
from typing import List
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, status

from core.dependencies import get_database, get_current_user, get_admin_user
from models.rss_feed import RssFeed
from models.subscriber import Subscriber
from services.rss_feed import RssFeedService
from services.rss_provider import RssProviderService

router = APIRouter(prefix="/rss_feeds", tags=["RSS Feed"])


@router.get("/", response_model=List[RssFeed])
async def list_rss_feeds(db=Depends(get_database)):
    """Gets a list of all rss feeds"""
    rss_feed_service = RssFeedService(db)
    rss_feeds = await rss_feed_service.list()
    return rss_feeds


@router.get("/{id}", response_model=RssFeed)
async def get_rss_feed_by_id(
    id: str,
    db=Depends(get_database),
    current_user: Subscriber = Depends(get_current_user),
):
    """Gets a rss feed by id"""
    rss_feed_service = RssFeedService(db)
    rss_feed = await rss_feed_service.get_by_id(id)
    return rss_feed


@router.get("{url}", response_model=RssFeed)
async def get_rss_feed_by_url(
    url: str,
    db=Depends(get_database),
    current_user: Subscriber = Depends(get_current_user),
):
    """Gets a rss feed by url"""
    rss_feed_service = RssFeedService(db)
    rss_feed = await rss_feed_service.get_by_url(url)
    return rss_feed


@router.get("/{provider_name}", response_model=List[RssFeed])
async def get_rss_feed_by_provider_name(
    provider_name: str,
    db=Depends(get_database),
    current_user: Subscriber = Depends(get_current_user),
):
    """Gets a rss feed by provider name"""
    rss_feed_service = RssFeedService(db)
    rss_provider_service = RssProviderService(db)
    rss_providers = await rss_provider_service.search_by_name(provider_name)

    rss_feeds = await asyncio.gather(
        *[
            rss_feed_service.get_by_provider_id(rss_provider.id)
            for rss_provider in rss_providers
        ]
    )
    return rss_feeds


@router.delete("/{id}", response_class=JSONResponse)
async def delete_rss_feed(
    id: str,
    db=Depends(get_database),
    current_user: Subscriber = Depends(get_admin_user),
):
    """Deletes a rss feed"""
    await RssFeedService(db).delete(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Rss feed deleted"}
    )
