from abc import ABCMeta, abstractmethod


class SiteMap(metaclass=ABCMeta):

    @property
    @abstractmethod
    def loc(self) -> str:
        pass

    @property
    @abstractmethod
    def lastmod(self) -> str:
        pass
