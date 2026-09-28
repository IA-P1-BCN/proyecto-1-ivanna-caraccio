from datetime import datetime, timedelta

from domain.race import Race
from domain.race_status import RaceStatus


def set_fixed_times(race, durations):
    current_start = datetime(2026, 1, 1, 12, 0, 0)

    for segment, seconds in zip(race.rate_segments, durations):
        segment.start_time = current_start
        segment.end_time = current_start + timedelta(seconds=seconds)
        current_start = segment.end_time


def build_finished_race(durations):
    race = Race()

    for _ in range(len(durations) - 1):
        if race.status == RaceStatus.STOPPED:
            race.change_status(RaceStatus.MOVING)
        else:
            race.change_status(RaceStatus.STOPPED)

    race.finish()
    set_fixed_times(race, durations)
    return race
