from services.utils.codec import PasswordCodec, TokenCodec
from database.subscriber import DBSubscriber
from models.subscriber import Subscriber
from core.config import settings
from urllib import parse

class AuthService:
    def __init__(self, db):
        self.db = db
        self.subscriber_db = DBSubscriber(db)

    async def login(self, username: str, password: str) -> bool:
        """
        Logs in a user
        """
        subscriber = await self.subscriber_db.get_by_username(username)
        if subscriber:
            if PasswordCodec().verify(password, subscriber.password):
                return True
            raise Exception("Invalid password")
        raise Exception("Invalid username")

    async def create_token_url(self, auth_path: str, subscriber: Subscriber) -> str:
        """
        Create token url for subscriber account
        """
        subscriber.id = str(subscriber.id)
        subscriber_dict = subscriber.dict(
            exclude={"password", "subscribed_blogs", "created_at"}
            )
        account_token = TokenCodec().encode(subscriber_dict)
        url = f"{settings.FRONTEND_URL}/{auth_path}?token={account_token}"
        return url

    async def confirm_account_activation(self, token: str) -> Subscriber:
        """
        Confirm account activation
        """
        subscriber_dict = TokenCodec().decode(token)
        subscriber = await self.subscriber_db.get_by_email(subscriber_dict["email"])
        if subscriber:
            subscriber.is_verified = True
            subscriber_update = await self.subscriber_db.update(subscriber.id, subscriber)
            return subscriber_update
        raise Exception("Invalid token")

    async def forgot_password(self, email: str) -> bool:
        """
        Forgot password
        """
        subscriber = await self.subscriber_db.get_by_email(email)
        if subscriber:
            return True
        raise Exception("Invalid username")