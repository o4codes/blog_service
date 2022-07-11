from typing import List

from bson import ObjectId
from core.config import settings
from models.rss_feed import RssFeed


class RssFeedDatabase:
    """Provides Database CRUD operations for rss feeds"""

    def __init__(self, db):
        self.db = db
        self.collection = self.db[settings.RSS_FEEDS_COLLECTION]

    async def list(self, **query) -> List[RssFeed]:
        """Gets a list of all rss feeds

        Args:
            query (dict): values to be used for filtering

        Returns:
            List[RssFeed]: list of rss feeds
        """
        rss_feeds = await self.collection.find(query).to_list(None)
        rss_feeds = [RssFeed(**rss_feed, id=rss_feed["_id"]) for rss_feed in rss_feeds]
        return rss_feeds

    async def count(self, **query) -> int:
        """Gets the count of rss feeds

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of rss feeds
        """
        return await self.collection.count_documents(query)

    async def get_by_id(self, feed_id: str) -> RssFeed:
        """
        Gets a rss feed by id

        Args:
            id (str): id of rss feed

        Returns:
            RssFeed: rss feed
            None: if no rss feed found
        """
        rss_feed = await self.collection.find_one({"_id": ObjectId(feed_id)})
        if rss_feed:
            return RssFeed(**rss_feed, id=rss_feed["_id"])
        return None

    async def get_by_provider_id(self, provider_id: str) -> List[RssFeed]:
        """
        Gets a list of rss feeds by provider id

        Args:
            provider_id (str): id of rss provider

        Returns:
            List[RssFeed]: list of rss feeds
        """
        rss_feeds = await self.collection.find(
            {"provider_id": ObjectId(provider_id)}
        ).to_list(None)
        rss_feeds = [RssFeed(**rss_feed, id=rss_feed["_id"]) for rss_feed in rss_feeds]
        return rss_feeds

    async def get_by_url(self, url: str) -> RssFeed:
        """
        Gets a rss feed by url

        Args:
            url (str): url of rss feed

        Returns:
            RssFeed: rss feed
            None: if no rss feed found
        """
        rss_feed = await self.collection.find_one({"link": url})
        if rss_feed:
            return RssFeed(**rss_feed, id=rss_feed["_id"])
        return None

    async def create(self, rss_feed: RssFeed) -> RssFeed:
        """
        Creates a rss feed

        Args:
            rss_feed (RssFeed): rss feed

        Returns:
            RssFeed: rss feed
        """
        result = await self.collection.insert_one(rss_feed.dict())
        rss_feed = await self.get_by_id(result.inserted_id)
        return rss_feed

    async def create_many(self, rss_feeds: List[RssFeed]) -> List[RssFeed]:
        """
        Creates a list of rss feeds

        Args:
            rss_feeds (List[RssFeed]): list of rss feeds

        Returns:
            List[RssFeed]: list of rss feeds
        """
        result = await self.collection.insert_many(
            [rss_feed.dict() for rss_feed in rss_feeds]
        )
        rss_feeds = [
            await self.get_by_id(result_id) for result_id in result.inserted_ids
        ]
        return rss_feeds

    async def update(self, feed_id, rss_feed: RssFeed) -> RssFeed:
        """
        Updates a rss feed

        Args:
            feed_id (str): id of rss feed
            rss_feed (RssFeed): rss feed

        Returns:
            RssFeed: rss feed
        """
        await self.collection.update_one(
            {"_id": ObjectId(feed_id)}, {"$set": rss_feed.dict(exclude={"id"})}
        )
        rss_feed = await self.get_by_id(feed_id)
        return rss_feed

    async def delete(self, feed_id: str) -> bool:
        """
        Deletes a rss feed

        Args:
            feed_id (str): id of rss feed

        Returns:
            bool: True if rss feed deleted, False otherwise
        """
        result = await self.collection.delete_one({"_id": ObjectId(feed_id)})
        return result.deleted_count > 0

    async def delete_many(self, provider_id: str) -> bool:
        """
        Deletes a list of rss feeds of a provider_id

        Args:
            provider_id (str): id of rss provider

        Returns:
            bool: True if rss feeds deleted, False otherwise
        """
        result = await self.collection.delete_many(
            {"provider_id": ObjectId(provider_id)}
        )
        return result.deleted_count > 0
