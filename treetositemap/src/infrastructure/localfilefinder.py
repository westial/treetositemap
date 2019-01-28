from glob import iglob

from ..domain.filefinder import FileFinder


class LocalFileFinder(FileFinder):

    def find_files(self, path_pattern: str, recursive: bool) -> list:
        return iglob(path_pattern, recursive=recursive)
