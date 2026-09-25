from datetime import datetime
from race_status import RaceStatus
from rate_segment import RateSegment


class Race:
    def __init__(self):
        self._start_time = datetime.now()
        self._status = RaceStatus.STOPPED
        self._rate_segments = [RateSegment(self._status, self._start_time)]

    @property
    def start_time(self):
        return self._start_time

    @property
    def status(self):
        return self._status

    @property
    def current_rate_segment(self):
        return self._rate_segments[-1]
