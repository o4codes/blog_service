from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from middlewares.error_handler import ErrorHandlerMiddleware
from core.config import settings
from application.routers import rss_provider, subscriber, rss_feed
from services.utils.mailing import send_mail




app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.SWAGGER_URL,
    redoc_url=settings.REDOC_URL,
)

@app.on_event("startup")
def startup():
    send_mail()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlerMiddleware, some_attribute="Error Handling Middleware")

app.include_router(subscriber.router, prefix=settings.API_V1_STR)
app.include_router(rss_provider.router, prefix=settings.API_V1_STR)
app.include_router(rss_feed.router, prefix=settings.API_V1_STR)


@app.get("/api/v1/ping")
async def ping():
    """
    Endpoint checks for
    1. Database connection
    2. Reachablity of 3rd party services
    """
    return {"ping": "pong"}


# mounts frontend folder to project
app.mount(
    "/",
    StaticFiles(directory="../frontend", html=True, check_dir=False),
    name="static",
)
