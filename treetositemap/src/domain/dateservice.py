from abc import ABCMeta, abstractmethod


class DateService(metaclass=ABCMeta):

    @abstractmethod
    def now_iso_format(self, with_micro: bool = False):
        pass
