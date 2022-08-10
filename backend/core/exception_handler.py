from bson.errors import InvalidId
from fastapi import status
from fastapi.responses import JSONResponse
from core.exceptions import (
    BadRequest,
    DatabaseException,
    ExistingDataException,
    NotFoundException,
    ForbiddenException,
    UnauthorizedException,
)


class AppExceptionHandler:
    """Base application exception handler"""

    def __init__(self, exception: Exception):
        self.message = str(exception)
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.headers = {}

        if isinstance(exception, NotFoundException):
            self.status_code = status.HTTP_404_NOT_FOUND

        if isinstance(exception, DatabaseException):
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exception, ExistingDataException):
            self.status_code = status.HTTP_409_CONFLICT

        if isinstance(exception, BadRequest) or isinstance(exception, InvalidId):
            self.status_code = status.HTTP_400_BAD_REQUEST

        if isinstance(exception, ForbiddenException):
            self.status_code = status.HTTP_403_FORBIDDEN

        if isinstance(exception, UnauthorizedException):
            self.status_code = status.HTTP_401_UNAUTHORIZED
            self.headers = ({"WWW-Authenticate": "Bearer"},)

    def raiseException(self):
        """Raises the exception with the appropriate status code"""
        message = {
            "status": "failed",
            "message": self.message,
        }
        return JSONResponse(
            status_code=self.status_code, content=message, headers=self.headers
        )
