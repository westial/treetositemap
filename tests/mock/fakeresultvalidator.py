from treetositemap.src.domain.resultvalidator import ResultValidator


class FakeResultValidator(ResultValidator):

    def is_valid(self, item_path) -> bool:
        return True
