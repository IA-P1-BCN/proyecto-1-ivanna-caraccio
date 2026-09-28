import pytest
from helpers import build_finished_race

from application.finish_race import FinishRace
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race import Race
from domain.race_status import RaceStatus
from interfaces.formatting import format_amount, format_duration


def test_finish_saves_the_end_time():
    race = Race()
    race.finish()
    assert race.end_time is not None
    assert race.end_time >= race.start_time


def test_finish_closes_every_segment():
    race = Race()
    race.change_status(RaceStatus.MOVING)
    race.finish()
    assert all(not s.is_open() for s in race.rate_segments)


def test_race_is_not_active_after_finishing():
    race = Race()
    assert race.is_active
    race.finish()
    assert not race.is_active


def test_finishing_twice_raises_an_error():
    race = Race()
    race.finish()
    with pytest.raises(ValueError):
        race.finish()


def test_cannot_change_status_of_a_finished_race():
    race = Race()
    race.finish()
    with pytest.raises(ValueError):
        race.change_status(RaceStatus.MOVING)


def test_amount_stops_growing_after_finishing():
    race = build_finished_race([10, 10])
    assert race.get_current_amount() == race.get_current_amount()


@pytest.mark.parametrize(
    "durations, expected_total",
    [
        ([10], 0.2),            # 10 s stopped
        ([10, 10], 0.7),        # 0.2 + 0.5
        ([10, 30, 20], 2.1),    # 0.2 + 1.5 + 0.4
        ([0, 60], 3.0),         # 0 + 3.0
        ([60, 0, 60], 2.4),     # 1.2 + 0 + 1.2
    ],
)
def test_total_amount_for_different_segment_combinations(durations, expected_total):
    race = build_finished_race(durations)
    assert race.get_current_amount() == pytest.approx(expected_total)


def test_total_duration_is_the_sum_of_the_segments():
    race = build_finished_race([10, 30, 20])
    assert race.get_duration_seconds() == pytest.approx(60)


def test_use_case_finishes_the_active_race(repository):
    session = RaceSession()
    StartRace(session).execute()

    race = FinishRace(session, repository).execute()

    assert race is not None
    assert race.end_time is not None


def test_use_case_frees_the_session(repository):
    session = RaceSession()
    StartRace(session).execute()

    FinishRace(session, repository).execute()

    assert session.active_race is None


def test_a_new_race_can_start_after_finishing(repository):
    session = RaceSession()
    StartRace(session).execute()
    FinishRace(session, repository).execute()

    new_race = StartRace(session).execute()

    assert new_race is not None


def test_finish_without_active_race_returns_none(repository):
    session = RaceSession()
    assert FinishRace(session, repository).execute() is None


def test_finish_without_active_race_shows_a_message(repository, capsys):
    FinishRace(RaceSession(), repository).execute()
    printed = capsys.readouterr().out
    assert "no hay ninguna carrera por terminar.\n" in printed.lower()


def test_finished_race_is_saved_in_the_history(repository):
    session = RaceSession()
    StartRace(session).execute()

    race = FinishRace(session, repository).execute()

    records = repository.get_all()
    assert len(records) == 1
    assert records[0].start_time == race.start_time
    assert records[0].end_time == race.end_time


@pytest.mark.parametrize(
    "amount, expected",
    [(2.1, "2.10€"), (0, "0.00€"), (0.456, "0.46€"), (12, "12.00€")],
)
def test_format_amount(amount, expected):
    assert format_amount(amount) == expected


@pytest.mark.parametrize(
    "seconds, expected",
    [(0, "00:00"), (5, "00:05"), (125, "02:05"), (3600, "60:00")],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected
