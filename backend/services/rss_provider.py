from typing import List

from database.rss_provider import RssProviderDatabase
from models.rss_provider import RssProvider

from services.utils.custom_exceptions import (
    DatabaseException,
    ExistingDataException,
    NotFoundException,
)
from services.utils.rss_utils import RSSUtils


class RssProviderService:
    def __init__(self, db):
        self.db = db
        self.rss_provider_db = RssProviderDatabase(db)

    async def list(self, **query) -> List[RssProvider]:
        """Gets a list of all rss providers

        Args:
            query (dict): values to be used for filtering

        Returns:
            List[RssProvider]: list of rss providers
        """
        rss_providers = await self.rss_provider_db.list(**query)
        return rss_providers

    async def count(self, **query) -> int:
        """Gets the count of rss providers

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of rss providers
        """
        return await self.rss_provider_db.count(**query)

    async def get_by_id(self, provider_id: str) -> RssProvider:
        """
        Gets a rss provider by id

        Args:
            id (str): id of rss provider

        Returns:
            RssProvider: rss provider
            None: if no rss provider found
        """
        rss_provider = await self.rss_provider_db.get_by_id(provider_id)
        if rss_provider:
            return rss_provider
        raise NotFoundException(f"Rss provider with id {provider_id} not found")

    async def create(self, url: str) -> RssProvider:
        """
        Creates a rss provider

        Args:
            url (str): url of rss provider

        Returns:
            RssProvider: rss provider
        """
        rss_provider = await self.rss_provider_db.get_by_url(url)
        if rss_provider is None:
            rss_util = await RSSUtils.async_init(url)
            rss_info = await rss_util.get_rss_info()
            print(rss_info)

            rss_provider = RssProvider(url=url, **rss_info)
            rss_provider = await self.rss_provider_db.create(rss_provider)
            if rss_provider:
                return rss_provider
            raise DatabaseException("Error creating rss provider")
        raise ExistingDataException(f"Rss provider with url '{url}' already exists")

    async def update(self, provider_id: str, url: str) -> RssProvider:
        """
        Updates a rss provider

        Args:
            id (str): id of rss provider
            url (str): url of rss provider

        Returns:
            RssProvider: rss provider
        """
        rss_provider = await self.rss_provider_db.get_by_id(provider_id)
        if rss_provider:
            rss_provider.url = url
            rss_provider = await self.rss_provider_db.update(rss_provider)
            return rss_provider
        raise NotFoundException(f"Rss provider with id {provider_id} not found")

    async def delete(self, provider_id: str) -> RssProvider:
        """
        Deletes a rss provider

        Args:
            id (str): id of rss provider

        Returns:
            RssProvider: rss provider
        """
        rss_provider = await self.rss_provider_db.get_by_id(provider_id)
        if rss_provider:
            result = await self.rss_provider_db.delete(rss_provider)
            if result:
                return rss_provider
            raise DatabaseException("Error deleting rss provider")
        raise NotFoundException(f"Rss provider with id {provider_id} not found")
