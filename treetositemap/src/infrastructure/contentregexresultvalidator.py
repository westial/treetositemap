import os
import re

from ..domain.resultvalidator import ResultValidator


class ContentRegexResultValidator(ResultValidator):

    def __init__(self, pattern_expression: str = None):
        self._pattern = re.compile(
            pattern_expression.encode(),
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )

    def is_valid(self, item_path) -> bool:
        if not os.path.isfile(item_path):
            return True
        with open(item_path, 'rb') as found_file:
            content = found_file.read()
            return bool(
                re.match(
                    self._pattern,
                    content
                )
            )
