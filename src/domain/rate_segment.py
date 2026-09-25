from .race_status import RaceStatus


class RateSegment:
    def __init__(self, status, start_time):
        self.status = status
        self.start_time = start_time
        self.end_time = None

    def is_open(self):
        return self.end_time is None

    def close(self, end_time):
        self.end_time = end_time
