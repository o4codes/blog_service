from services.utils.custom_exceptions import * 
from fastapi import HTTPException, status
from bson.errors import InvalidId

class AppExceptionHandler:
    """Base application exception handler
    """
    
    def __init__(self, exception: Exception):
        self.message = str(exception)
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exception, NotFoundException):
            self.status_code = status.HTTP_404_NOT_FOUND     
        
        if isinstance(exception, DatabaseException):
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exception, ExistingDataException):
            self.status_code = status.HTTP_400_BAD_REQUEST

        if isinstance(exception, InvalidId):
            self.status_code = status.HTTP_400_BAD_REQUEST

        if isinstance(exception, BadRequest):
            self.status_code = status.HTTP_400_BAD_REQUEST

    def raiseException(self):
        raise HTTPException(status_code=self.status_code, detail=self.message)