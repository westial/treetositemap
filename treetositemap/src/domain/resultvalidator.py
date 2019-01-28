from abc import ABCMeta, abstractmethod


class ResultValidator(metaclass=ABCMeta):

    @abstractmethod
    def is_valid(self, book_content) -> bool:
        pass
