from services.utils.codec import PasswordCodec
from services.utils.mailing import send_mail
from database.subscriber import DBSubscriber

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

    async def forgot_password(self, email: str) -> bool:
        """
        Forgot password
        """
        subscriber = await self.subscriber_db.get_by_email(email)
        if subscriber:
            return True
        raise Exception("Invalid username")