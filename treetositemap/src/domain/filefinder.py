from abc import ABCMeta, abstractmethod


class FileFinder(metaclass=ABCMeta):

    @abstractmethod
    def find_files(self, path_pattern: str, recursive: bool) -> list:
        """
        :param recursive: recursively
        :param path_pattern: Unix style pathname pattern expansion
        :return: paths
        """
        pass
