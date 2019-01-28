from abc import ABCMeta, abstractmethod

from .dto.sitemap import SiteMap
from .dto.url import Url


class SiteMapRepository(metaclass=ABCMeta):

    @abstractmethod
    def count_urls(self) -> int:
        pass

    @abstractmethod
    def count_sitemaps(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def add_url(self, url: Url):
        pass

    @abstractmethod
    def add_sitemap(self, sitemap: SiteMap):
        pass

    @abstractmethod
    def get_urlsets(self, url_set_size: int) -> list:
        pass

    @abstractmethod
    def get_sitemaps(self) -> list:
        pass
