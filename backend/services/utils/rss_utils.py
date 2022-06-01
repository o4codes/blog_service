from pprint import pprint
import aiohttp
import feedparser
from .custom_exceptions import BadRequest

class RSSUtils:

    @classmethod
    async def __get_rss_data(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    response = await response.text()
                    rss_data = feedparser.parse(response)
                    return rss_data
                raise BadRequest('RSS url is not accessible')

    def __init__(self, url):
        self.url = url
        self.rss_data = None


    @classmethod
    async def async_init(cls, url) -> 'RSSUtils': 
        self = cls(url)
        rss_data = await cls.__get_rss_data(url)
        self.rss_data = rss_data
        return self
    
            
    async def get_rss_info(self) -> dict:
        rss_info = {}
        rss_info['title'] = self.rss_data.feed.title
        rss_info['link'] = self.rss_data.feed.link
        rss_info['description'] = self.rss_data.feed.description
        rss_info['image'] = self.rss_data.feed.image.url
        return rss_info

    async def get_rss_items(self):
        self.rss_items = self.rss_data.entries

    async def get_rss_item_data(self, rss_item):
        rss_item_data = {}
        rss_item_data['title'] = rss_item.title
        rss_item_data['link'] = rss_item.link
        rss_item_data['description'] = rss_item.description
        rss_item_data['published'] = rss_item.published
        return rss_item_data