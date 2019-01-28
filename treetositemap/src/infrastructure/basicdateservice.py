from datetime import datetime

from ..domain.dateservice import DateService


class BasicDateService(DateService):

    def now_iso_format(self, with_micro: bool = False):
        date_format = '%Y-%m-%dT%H:%M:%S'
        if with_micro:
            date_format += ".%f"
            result = datetime.utcnow().strftime(date_format)[:-3]
        else:
            result = datetime.utcnow().strftime(date_format)
        return result + 'Z'
