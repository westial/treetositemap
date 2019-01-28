from ...domain.dto.url import Url


class XmlUrl(Url):

    def __init__(self, loc: str):
        self.__loc = loc

    @property
    def loc(self) -> str:
        return self.__loc
