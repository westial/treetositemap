from typing import List

from ..domain.dto.sitemap import SiteMap
from ..domain.dto.url import Url
from ..domain.sitemaprepository import SiteMapRepository


class InMemorySiteMapRepository(SiteMapRepository):

    def __init__(self):
        self.__sitemaps: List[SiteMap] = list()
        self.__urls: List[Url] = list()

    def count_urls(self) -> int:
        return len(self.__urls)

    def count_sitemaps(self) -> int:
        return len(self.__sitemaps)

    def is_empty(self) -> bool:
        return not self.count_urls()

    def add_url(self, url: Url):
        self.__urls.append(url)

    def add_sitemap(self, sitemap: SiteMap):
        self.__sitemaps.append(sitemap)

    def get_urlsets(self, url_set_size: int) -> list:
        for chunk in self.__chunks(self.__urls, url_set_size):
            yield chunk

    def get_sitemaps(self) -> list:
        for sitemap in self.__sitemaps:
            yield sitemap

    @classmethod
    def __chunks(cls, items: list, size) -> list:
        for index in range(0, len(items), size):
            yield items[index: index + size]
