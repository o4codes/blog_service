from typing import List

from database.rss_feed import RssFeedDatabase
from models.rss_feed import RssFeed
from services.utils.rss_utils import RSSUtils
from core.custom_exceptions import (
    NotFoundException,
    DatabaseException,
    ExistingDataException,
)


class RssFeedService:
    def __init__(self, db):
        self.db = db
        self.rss_feed_db = RssFeedDatabase(db)

    async def list(self, **query) -> List[RssFeed]:
        """Gets a list of all rss feeds

        Args:
            query (dict): values to be used for filtering

        Returns:
            List[RssFeed]: list of rss feeds
        """
        rss_feeds = await self.rss_feed_db.list(**query)
        return rss_feeds

    async def count(self, **query) -> int:
        """Gets the count of rss feeds

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of rss feeds
        """
        return await self.rss_feed_db.count(**query)

    async def get_by_id(self, id: str) -> RssFeed:
        """
        Gets a rss feed by id

        Args:
            id (str): id of rss feed

        Returns:
            RssFeed: rss feed
            None: if no rss feed found
        """
        rss_feed = await self.rss_feed_db.get_by_id(id)
        if rss_feed:
            return rss_feed
        raise NotFoundException(f"Rss feed with id {id} not found")

    async def get_by_url(self, url: str) -> RssFeed:
        """
        Gets a rss feed by url

        Args:
            url (str): url of rss feed

        Returns:
            RssFeed: rss feed
        """
        rss_feed = await self.rss_feed_db.get_by_url(url)
        if rss_feed:
            return rss_feed
        raise NotFoundException(f"Rss feed with url {url} not found")

    async def get_by_provider_id(self, url: str) -> RssFeed:
        """
        Gets a rss feed by provider url

        Args:
            url (str): url of rss provider

        Returns:
            RssFeed: rss feed
            None: if no rss feed found
        """
        rss_feed = await self.rss_feed_db.get_by_provider_id(url)
        if rss_feed:
            return rss_feed
        raise NotFoundException(f"Rss feed with url {url} not found")

    async def create(self, rss_feed: RssFeed) -> RssFeed:
        """
        Creates a rss feed

        Args:
            rss_feed (RssFeed): rss feed

        Returns:
            RssFeed: rss feed
        """
        rss_feed = await self.rss_feed_db.create(rss_feed)
        if rss_feed:
            return rss_feed
        raise DatabaseException("Error creating rss feed")

    async def create_many(self, rss_feeds: List[RssFeed]) -> List[RssFeed]:
        """
        Creates a list of rss feeds

        Args:
            rss_feeds (List[RssFeed]): list of rss feeds

        Returns:
            List[RssFeed]: list of rss feeds
        """
        rss_feeds = await self.rss_feed_db.create_many(rss_feeds)
        if rss_feeds:
            return rss_feeds
        raise DatabaseException("Error creating rss feeds")

    async def update(self, id: str, rss_feed: RssFeed) -> RssFeed:
        """
        Updates a rss feed

        Args:
            id (str): id of rss feed
            rss_feed (RssFeed): rss feed

        Returns:
            RssFeed: rss feed
        """
        if await self.rss_feed_db.get_by_id(id) is not None:
            if await self.rss_feed_db.get_by_url(rss_feed.link) is None:
                rss_feed = await self.rss_feed_db.update(id, rss_feed)
                if rss_feed:
                    return rss_feed
            raise ExistingDataException(
                f"Rss feed with url {rss_feed.link} already exists"
            )
        raise NotFoundException(f"Rss feed with id {id} not found")

    async def delete(self, id: str) -> bool:
        """
        Deletes a rss feed

        Args:
            id (str): id of rss feed

        Returns:
            bool: True if rss feed deleted, False otherwise
        """
        if await self.rss_feed_db.get_by_id(id) is not None:
            deleted = await self.rss_feed_db.delete(id)
            if deleted:
                return True
            raise DatabaseException("Error deleting rss feed")
        raise NotFoundException(f"Rss feed with id {id} not found")
