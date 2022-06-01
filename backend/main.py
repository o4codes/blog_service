from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from services.utils.rss_utils import RSSUtils
from pprint import pprint
from core.config import settings
from application.routers import (
    subscriber,
    rss_provider
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION, 
    version=settings.PROJECT_VERSION,
    docs_url=settings.SWAGGER_URL,
    redoc_url=settings.REDOC_URL,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscriber.router, prefix=settings.API_V1_STR)
app.include_router(rss_provider.router, prefix=settings.API_V1_STR)


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