import os
from datetime import datetime


def replace_root_directory_path(
        root_directory: str,
        original_path: str,
        replacement_path: str
):
    relative_path = os.path.relpath(original_path, start=root_directory)
    return join_paths(replacement_path, relative_path)


def clean_path(path: str, is_relative: bool = False):
    if is_relative:
        if path[0] == os.sep:
            path = path[1:]
        elif path[:2] == "{0}{1}".format(".", os.sep):
            path = path[2:]
    if path[-1] == os.sep:
        path = path[:-1]
    return path


def join_paths(*paths, is_relative: bool = False):
    clean_paths = list()
    for path in paths:
        if not clean_paths:
            path = clean_path(path, is_relative)
        else:
            path = clean_path(path, True)
        clean_paths.append(path)
    result_path = os.path.join(*clean_paths)
    return result_path
