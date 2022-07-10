from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.exception_handler import AppExceptionHandler

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        
        try:
            # process the request and get the response    
            response = await call_next(request)
            return response
        except Exception as e:
            print(e)
            raise AppExceptionHandler(e).raiseException()
