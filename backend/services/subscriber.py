from typing import List

from database.subscriber import DBSubscriber
from models.subscriber import Subscriber

from .utils.custom_exceptions import (
    DatabaseException,
    ExistingDataException,
    NotFoundException,
)


class SubscriberService:
    def __init__(self, database):
        self.database = database
        self.subscriber_db = DBSubscriber(self.database)


    async def list(self, **query) -> List[Subscriber]:
        """Gets a list of all subscrubers

        Args:
            query (dict): values to be used for filtering

        Returns:
            List[Subscriber]: list of subscribers
        """
        subscribers = await self.subscriber_db.list(**query)
        return subscribers


    async def count(self, **query) -> int:
        """Gets the count of subscribers

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of subscribers
        """
        return await self.subscriber_db.count(**query)


    async def get_by_email(self, email) -> Subscriber:
        """Gets a subscriber by email

        Args:
            email (str): email of subscriber

        Returns:
            Subscriber: subscriber
            None: if no subscriber found

        Raises:
            NotFoundException: if subscriber not found
        """
        subscriber = await self.subscriber_db.get_by_email(email)
        if subscriber:
            return subscriber
        raise NotFoundException(f"Subscriber with email {email} not found")


    async def get_by_id(self, id: str) -> Subscriber:
        """Gets a subscriber by id

        Args:
            id (str): id of subscriber

        Returns:
            Subscriber: subscriber

        Raises:
            NotFoundException: if subscriber not found
        """
        subscriber = await self.subscriber_db.get_by_id(id)
        if subscriber:
            return subscriber
        raise NotFoundException(f"Subscriber with id {id} not found")


    async def create(self, email: str) -> Subscriber:
        """Creates a subscriber

        Args:
            subscriber (Subscriber): subscriber to be created

        Returns:
            Subscriber: created subscriber

        Raises:
            ExistingDataException: if subscriber with email already exists
            DatabaseException: if failed to create subscriber
        """
        email_search = await self.subscriber_db.get_by_email(email)
        if email_search:
            raise ExistingDataException(f"Subscriber with email {email} already exists")

        subscriber = Subscriber(email=email)
        subscriber = await self.subscriber_db.create(subscriber)
        if subscriber:
            return subscriber
        raise DatabaseException("Failed to create subscriber")


    async def update(self, id: str, subscriber: Subscriber) -> Subscriber:
        """Updates a subscriber

        Args:
            subscriber (Subscriber): subscriber to be updated

        Returns:
            Subscriber: updated subscriber

        Raises:
            NotFoundException: if subscriber not found
            DatabaseException: if failed to update subscriber
            ExistingDataException: if subscriber with email already exists
        """
        db_subscriber = await self.subscriber_db.get_by_id(id)
        if db_subscriber is None:
            raise NotFoundException(f"Subscriber with id {subscriber.id} not found")

        email_search = await self.subscriber_db.get_by_email(subscriber.email)
        if (email_search and email_search.id == subscriber.id) or (
            email_search is None
        ):
            subscriber = await self.subscriber_db.update(id, subscriber)
            if subscriber:
                return Subscriber(**subscriber)
            raise DatabaseException("Failed to update subscriber")
        raise ExistingDataException(
            f"Subscriber with email {subscriber.email} already exists"
        )


    async def delete(self, id: str) -> bool:
        """Deletes a subscriber by id

        Args:
            id (str): id of subscriber

        Returns:
            bool: True if deleted, False if not

        Raises:
            NotFoundException: if subscriber not found
            DatabaseException: if failed to delete subscriber
        """
        db_subscriber = await self.subscriber_db.get_by_id(id)
        if db_subscriber is None:
            raise NotFoundException(f"Subscriber with id {id} not found")
        result = await self.subscriber_db.delete(id)
        if result:
            return True
        raise DatabaseException("Failed to delete subscriber")
