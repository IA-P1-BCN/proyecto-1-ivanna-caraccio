from datetime import datetime
from .race_status import RaceStatus
from .rate_segment import RateSegment
from .rates import RATE_PER_SECOND


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

    @property
    def rate_segments(self):
        return list(self._rate_segments)

    def get_current_amount(self):
        now = datetime.now()
        total = 0.0

        for segment in self._rate_segments:
            price_per_second = RATE_PER_SECOND[segment.status]
            total += segment.get_duration_seconds(now) * price_per_second

        return total
    
    def change_status(self, new_status):
        if new_status == self._status: return
        
        now = datetime.now()
        self.current_rate_segment.close(now)
        self._status = new_status
        new_segment = RateSegment(new_status, now)
        self._rate_segments.append(new_segment)
        
