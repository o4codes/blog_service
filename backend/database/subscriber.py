from core.config import settings
from typing import List
from bson import ObjectId


from models.subscriber import Subscriber

class DBSubscriber:
    def __init__(self, db):
        self.db = db
        self.collection = self.db[settings.SUBSCRIBER_COLLECTION]
    
    async def list(self, **query) -> List[Subscriber]:
        """ Gets a list of all subscrubers
        
        Args:
            query (dict): values to be used for filtering

        Returns:
            List[Subscriber]: list of subscribers
        """
        subscribers = await self.collection.find(query).to_list(None)
        subscribers = [Subscriber(**subscriber, id=subscriber['_id']) for subscriber in subscribers]
        return subscribers


    async def count(self, **query) -> int:
        """ Gets the count of subscribers

        Args:
            query (dict): values to be used for filtering

        Returns:
            int: count of subscribers
        """
        return await self.collection.count_documents(query)

    
    async def get_by_email(self, email) -> Subscriber:
        """ Gets a subscriber by email

        Args:
            email (str): email of subscriber

        Returns:
            Subscriber: subscriber
            None: if no subscriber found
        """
        subscriber = await self.collection.find_one({"email": email})
        if subscriber:
            return Subscriber(**subscriber, id=subscriber['_id'])
        return None


    async def get_by_id(self, id: str) -> Subscriber:
        """
        Gets a subscriber by id

        Args:
            id (str): id of subscriber

        Returns:
            Subscriber: subscriber
            None: if no subscriber found
        """
        subscriber = await self.collection.find_one({"_id": ObjectId(id)})
        if subscriber:
            return Subscriber(**subscriber, id=subscriber['_id'])
        return None
    

    async def create(self, subscriber: Subscriber) -> Subscriber:
        """ Creates a new subscriber

        Args:
            Subscriber (Subscriber): subscriber to be created

        Returns:
            Subscriber: created subscriber
        """
        result = await self.collection.insert_one(subscriber.dict(exclude={'id'}))
        subscriber = await self.get_by_id(result.inserted_id)
        return subscriber


    async def update(self,id: str, subscriber: Subscriber) -> Subscriber:
        """ Updates a subscriber

        Args:
            id (str): id of subscriber to be updated
            Subscriber (Subscriber): subscriber with updated values

        Returns:
            Subscriber: updated subscriber
        """
        await self.collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": subscriber.dict(exclude={"id"})}
            )
        subscriber = await self.get_by_id(id)
        return subscriber


    async def delete(self, id: str) -> bool:
        """ Deletes a subscriber

        Args:
            id (str): id of subscriber to be deleted

        Returns:
            bool: True if deleted, False if not
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0