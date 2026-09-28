from datetime import datetime
from .race_status import RaceStatus
from .rate_segment import RateSegment
from .rates import RATE_PER_SECOND
from .race_record import RaceRecord


class Race:
    def __init__(self):
        self._start_time = datetime.now()
        self._end_time = None
        self._status = RaceStatus.STOPPED
        self._rate_segments = [RateSegment(self._status, self._start_time)]

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def status(self):
        return self._status

    @property
    def is_active(self):
        return self._end_time is None

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

    def get_duration_seconds(self):
        now = datetime.now()
        return sum(s.get_duration_seconds(now) for s in self._rate_segments)

    def change_status(self, new_status):
        if not self.is_active:
            raise ValueError(
                "No se puede cambiar el estado a una carrera terminada.")

        if new_status == self._status:
            return

        now = datetime.now()
        self.current_rate_segment.close(now)
        self._status = new_status
        new_segment = RateSegment(new_status, now)
        self._rate_segments.append(new_segment)

    def finish(self):
        if not self.is_active:
            raise ValueError("La carrera ya terminó.")

        now = datetime.now()
        self.current_rate_segment.close(now)
        self._end_time = now

    def to_record(self):
        if self.is_active:
            raise ValueError(
                "Solo se puede guardar el registro de una carrera finalizada.")

        return RaceRecord(
            start_time=self._start_time,
            end_time=self._end_time,
            duration_seconds=round(self.get_duration_seconds(), 2),
            total_amount=round(self.get_current_amount(), 2),
        )
