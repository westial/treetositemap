from treetositemap.src.domain.dateservice import DateService


class MockDateService(DateService):

    def __init__(self, forced):
        self.__forced = forced

    def now_iso_format(self, with_micro: bool = False):
        return self.__forced
