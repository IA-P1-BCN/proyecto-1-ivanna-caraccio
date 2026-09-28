import pytest
from helpers import set_fixed_times

from application.change_race_status import ChangeRaceStatus
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race import Race
from domain.race_status import RaceStatus


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
    race = Race()
    race.change_status(RaceStatus.MOVING)
    race.change_status(RaceStatus.STOPPED)

    set_fixed_times(race, [10, 30, 20])

    assert race.get_current_amount() == pytest.approx(2.1)


def test_status_change_does_not_reset_the_accumulated_amount():
    race = Race()
    race.change_status(RaceStatus.MOVING)

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
