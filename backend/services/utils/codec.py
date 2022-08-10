from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

from core.config import settings
from core.exceptions import BadRequest


class PasswordCodec:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password):
        return self.pwd_context.hash(password)

    def verify(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)


class TokenCodec:
    def __init__(self):
        pass

    def encode(self, payload: dict) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.AUTH_EXP_TIME)
        payload_copy = payload.copy()
        payload_copy["exp"] = expires_delta
        return jwt.encode(
            payload_copy, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except JWTError as e:
            raise BadRequest("Invalid token") from e
