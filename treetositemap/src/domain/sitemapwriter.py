from abc import ABCMeta, abstractmethod
from typing import List

from .dto.sitemap import SiteMap
from .dto.url import Url


class SiteMapWriter(metaclass=ABCMeta):

    @abstractmethod
    def write_urlset(self, file_path: str, urls: List[Url]):
        pass

    @abstractmethod
    def write_sitemapindex(self, file_path: str, sitemaps: List[SiteMap]):
        pass

