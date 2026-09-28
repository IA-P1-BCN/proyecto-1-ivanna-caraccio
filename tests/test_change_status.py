from datetime import datetime, timedelta

import pytest

from application.change_race_status import ChangeRaceStatus
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race import Race
from domain.race_status import RaceStatus


def set_fixed_times(race, durations):
    
    current_start = datetime(2026, 1, 1, 12, 0, 0)

    for segment, seconds in zip(race.rate_segments, durations):
        segment.start_time = current_start
        segment.end_time = current_start + timedelta(seconds=seconds)
        current_start = segment.end_time



def test_change_status_updates_the_race_status():
    race = Race()
    race.change_status(RaceStatus.MOVING)
    assert race.status == RaceStatus.MOVING


def test_change_status_closes_old_segment_and_opens_a_new_one():
    race = Race()
    race.change_status(RaceStatus.MOVING)

    segments = race.rate_segments
    assert len(segments) == 2
    assert not segments[0].is_open()
    assert segments[1].is_open()
    assert segments[1].status == RaceStatus.MOVING


def test_change_to_the_same_status_does_not_add_a_segment():
    race = Race()
    race.change_status(RaceStatus.STOPPED)  # already stopped
    assert len(race.rate_segments) == 1


def test_amount_is_accumulated_per_segment():
    # stopped -> moving -> stopped
    race = Race()
    race.change_status(RaceStatus.MOVING)
    race.change_status(RaceStatus.STOPPED)

    # 10 s stopped + 30 s moving + 20 s stopped
    set_fixed_times(race, [10, 30, 20])

    # 10 * 0.02 + 30 * 0.05 + 20 * 0.02 = 0.2 + 1.5 + 0.4 = 2.1
    assert race.get_current_amount() == pytest.approx(2.1)


def test_status_change_does_not_reset_the_accumulated_amount():
    race = Race()
    race.change_status(RaceStatus.MOVING)

    # 10 s stopped (0.2 €) + 10 s moving (0.5 €)
    set_fixed_times(race, [10, 10])

    assert race.get_current_amount() == pytest.approx(0.7)


def test_use_case_changes_the_status_of_the_active_race():
    session = RaceSession()
    StartRace(session).execute()

    ChangeRaceStatus(session).execute(RaceStatus.MOVING)

    assert session.active_race.status == RaceStatus.MOVING



def test_change_status_without_active_race_returns_none():
    session = RaceSession()  # no race started

    result = ChangeRaceStatus(session).execute(RaceStatus.MOVING)

    assert result is None


def test_change_status_without_active_race_does_not_create_a_race():
    session = RaceSession()

    ChangeRaceStatus(session).execute(RaceStatus.MOVING)

    assert session.active_race is None


def test_change_status_without_active_race_shows_a_message(capsys):
    session = RaceSession()

    ChangeRaceStatus(session).execute(RaceStatus.MOVING)

    printed = capsys.readouterr().out
    assert "no hay carrera activa. empieza una primero.\n" in printed.lower()
