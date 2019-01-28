from ..domain.resultvalidator import ResultValidator


class FakeResultValidator(ResultValidator):

    def is_valid(self, book_content) -> bool:
        # TODO
        return True
