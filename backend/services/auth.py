from services.utils.codec import PasswordCodec, TokenCodec
from database.subscriber import DBSubscriber
from models.subscriber import Subscriber
from core.config import settings
from core.custom_exceptions import BadRequest, UnauthorizedException


class AuthService:
    def __init__(self, db):
        self.db = db
        self.subscriber_db = DBSubscriber(db)

    async def login(self, email: str, password: str) -> bool:
        """
        Logs in a user
        """
        subscriber = await self.subscriber_db.get_by_email(email)
        if subscriber:
            if PasswordCodec().verify(password, subscriber.password):
                if subscriber.is_verified:
                    return True
                raise UnauthorizedException("Account is not verified")
            raise BadRequest("Invalid password")
        raise BadRequest("Invalid username")

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

    async def verify_account(self, token: str) -> Subscriber:
        """
        Confirm account activation
        """
        subscriber_dict = TokenCodec().decode(token)
        subscriber = await self.subscriber_db.get_by_email(subscriber_dict["email"])
        if subscriber:
            subscriber.is_verified = True
            subscriber_update = await self.subscriber_db.update(
                subscriber.id, subscriber
            )
            return subscriber_update
        raise Exception("Invalid token")

    async def reset_password(self, token: str, password: str) -> Subscriber:
        """
        Reset password
        """
        subscriber_dict = TokenCodec().decode(token)
        subscriber = await self.subscriber_db.get_by_email(subscriber_dict["email"])
        if subscriber:
            subscriber.password = PasswordCodec().encode(password)
            subscriber_update = await self.subscriber_db.update(
                subscriber.id, subscriber
            )
            return subscriber_update
        raise Exception("Invalid token")
