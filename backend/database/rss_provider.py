from typing import List, Union

from bson import ObjectId
from core.config import settings
from models.rss_provider import RssProvider


class RssProviderDatabase:
    """Provides Database CRUD operations for rss providers"""

    def __init__(self, db):
        self.db = db
        self.collection = self.db[settings.RSS_PROVIDER_COLLECTION]

    async def list(self, **query) -> List[RssProvider]:
        """Gets a list of all rss providers

        Args:
            query (dict): values to be used for filtering

        Returns:
            List[Subscriber]: list of subscribers
        """
        rss_providers = await self.collection.find(query).to_list(None)
        rss_providers = [
            RssProvider(**rss_provider, id=rss_provider["_id"])
            for rss_provider in rss_providers
        ]
        return rss_providers

    async def count(self, **query) -> int:
        """Gets the count of rss providers

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of subscribers
        """
        return await self.collection.count_documents(query)

    async def get_by_id(self, provider_id: str) -> Union[RssProvider,None]:
        """
        Gets a rss provider by id

        Args:
            id (str): id of rss provider

        Returns:
            RssProvider: rss provider
            None: if no rss provider found
        """
        rss_provider = await self.collection.find_one({"_id": ObjectId(provider_id)})
        if rss_provider:
            return RssProvider(**rss_provider, id=rss_provider["_id"])
        return None

    async def get_by_url(self, url: str) -> RssProvider:
        """
        Gets a rss provider by url

        Args:
            url (str): url of rss provider

        Returns:
            RssProvider: rss provider
            None: if no rss provider found
        """
        rss_provider = await self.collection.find_one({"url": url})
        if rss_provider:
            return RssProvider(**rss_provider, id=rss_provider["_id"])
        return None

    async def search_by_name(self, name: str) -> List[RssProvider]:
        """
        Searches for rss providers by name

        Args:
            name (str): name of rss provider

        Returns:
            List[RssProvider]: list of rss providers
        """
        rss_providers = await self.collection.find(
            {"name": {"$regex": f"/{name}$/i"}}
        ).to_list(None)
        rss_providers = [
            RssProvider(**rss_provider, id=rss_provider["_id"])
            for rss_provider in rss_providers
        ]
        return rss_providers

    async def create(self, rss_provider: RssProvider) -> RssProvider:
        """
        Creates a rss provider

        Args:
            rss_provider (RssProvider): rss provider

        Returns:
            RssProvider: rss provider
        """
        result = await self.collection.insert_one(rss_provider.dict(exclude={"id"}))
        rss_provider = await self.get_by_id(result.inserted_id)
        return rss_provider

    async def update(self, provider_id: str, rss_provider: RssProvider) -> RssProvider:
        """
        Updates a rss provider

        Args:
            id (str): id of rss provider
            rss_provider (RssProvider): rss provider

        Returns:
            RssProvider: rss provider
        """
        await self.collection.update_one(
            {"_id": ObjectId(provider_id)}, {"$set": rss_provider.dict(exclude={"id"})}
        )
        rss_provider = await self.get_by_id(id)
        return rss_provider

    async def delete(self, provider_id: str) -> bool:
        """
        Deletes a rss provider

        Args:
            id (str): id of rss provider

        Returns:
            bool: True if rss provider was deleted, False otherwise
        """
        result = await self.collection.delete_one({"_id": ObjectId(provider_id)})
        return result.deleted_count > 0
