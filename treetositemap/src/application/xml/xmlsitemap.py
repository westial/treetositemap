from ...domain.dto.sitemap import SiteMap


class XmlSiteMap(SiteMap):

    def __init__(self, loc: str, lastmod: str):
        self.__loc = loc
        self.__lastmod = lastmod

    @property
    def loc(self) -> str:
        return self.__loc

    @property
    def lastmod(self) -> str:
        return self.__lastmod
