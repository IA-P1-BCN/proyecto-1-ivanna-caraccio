import time
from datetime import datetime

import pytest

from domain.race import Race
from domain.race_status import RaceStatus


def test_race_starts_with_stopped_status():
    race = Race()
    assert race.status == RaceStatus.STOPPED


def test_race_has_a_start_time():
    race = Race()
    assert isinstance(race.start_time, datetime)


def test_race_starts_with_a_single_open_rate_segment():
    race = Race()
    assert len(race.rate_segments) == 1
    assert race.rate_segments[0].is_open()


def test_amount_is_almost_zero_right_after_start():
    race = Race()
    amount = race.get_current_amount()
    assert amount == pytest.approx(0, abs=0.01)


def test_amount_grows_using_the_stopped_rate():
    race = Race()
    time.sleep(1)
    amount = race.get_current_amount()
    assert amount == pytest.approx(0.02, abs=0.01)
