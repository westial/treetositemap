from abc import ABCMeta, abstractmethod


class Url(metaclass=ABCMeta):

    @property
    @abstractmethod
    def loc(self) -> str:
        pass
