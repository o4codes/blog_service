import asyncio
from sched import scheduler
from typing import List
from functools import reduce

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient
from pytz import utc

from core.config import settings
from core.dependencies import get_database
from models.rss_provider import RssProvider
from models.rss_feed import RssFeed
from services.rss_provider import RssProviderService
from services.rss_feed import RssFeedService
from services.utils.rss_utils import RSSUtils


class FeedScheduler:
    def __init__(self):
        self.__client = MongoClient(settings.DATABASE_URL)
        self.__jobstores = {
            "default": MongoDBJobStore(
                database=settings.DATABASE_NAME,
                collection="scheduler_jobs",
                client=self.__client,
            )
        }
        self.__executors = {
            "default": ThreadPoolExecutor(20),
            "processpool": ProcessPoolExecutor(5),
        }
        self.scheduler = AsyncIOScheduler(
            jobstores=self.__jobstores,
            executors=self.__executors,
            job_defaults={"coalesce": False, "max_instances": 3},
            timezone=utc,
        )

    @classmethod
    async def get_latest_provider_feeds(cls, provider: RssProvider = None):
        """This gets the latest feeds from the provider

        Arguments:
            provider {RssProvider} -- The provider to get the latest feeds from

        Returns:
            List[RssFeed] -- The latest feeds from the provider
        """
        rss_util = await RSSUtils.async_init(provider.url)
        rss_feeds = await rss_util.get_rss_items()
        parsed_rss_feeds: List[RssFeed] = [
            RssFeed(**feed, provider_id=provider.id) for feed in rss_feeds
        ]
        if provider.last_feed_time:
            parsed_rss_feeds = [
                feed
                for feed in parsed_rss_feeds
                if feed.published_date > provider.last_feed_time
            ]

        latest_feed = reduce(
            lambda feed1, feed2: feed1
            if feed1.published_date > feed2.published_date
            else feed2,
            parsed_rss_feeds,
        )
        await RssProviderService(get_database()).update_last_feed_time(
            provider.id, latest_feed.published_date
        )
        rss_feeds_saved = await RssFeedService(get_database()).create_many(
            parsed_rss_feeds
        )
        return rss_feeds_saved

    @classmethod
    async def job_init_func(cls):
        """This initializes the job to run"""
        providers = await RssProviderService(get_database()).list()
        if providers:
            results = await asyncio.gather(
                *[cls.get_latest_provider_feeds(provider) for provider in providers]
            )
            print("scheduled job is done running")

    def start(self, func):
        self.scheduler.start()
        print("scheduler started")
        if self.scheduler.get_job("feed_scheduler") is None:
            self.scheduler.add_job(func, "interval", hours=1, id="feed_scheduler")
            print("scheduled job added")

    def shutdown(self):
        self.scheduler.shutdown()
        print("scheduler shutdown")


feed_scheduler = FeedScheduler()
