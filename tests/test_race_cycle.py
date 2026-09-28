import pytest

from application.change_race_status import ChangeRaceStatus
from application.finish_race import FinishRace
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race_status import RaceStatus
from helpers import set_fixed_times


def run_race(session, new_statuses, durations):
    StartRace(session).execute()
    change_status = ChangeRaceStatus(session)

    for status in new_statuses:
        change_status.execute(status)

    race = FinishRace(session).execute()
    set_fixed_times(race, durations)
    return race


def test_new_race_starts_clean_after_a_previous_one():
    session = RaceSession()
    first = run_race(session, [RaceStatus.MOVING], [10, 10])

    second = StartRace(session).execute()

    assert second is not first
    assert second.status == RaceStatus.STOPPED
    assert len(second.rate_segments) == 1
    assert second.get_current_amount() == pytest.approx(0, abs=0.05)


def test_consecutive_races_have_independent_amounts():
    session = RaceSession()

    first = run_race(session, [RaceStatus.MOVING], [10, 10])  # 0.2 + 0.5
    second = run_race(session, [], [20])                      # 0.4

    assert first.get_current_amount() == pytest.approx(0.7)
    assert second.get_current_amount() == pytest.approx(0.4)


def test_history_keeps_every_finished_race_in_order():
    session = RaceSession()

    first = run_race(session, [], [10])
    second = run_race(session, [], [20])
    third = run_race(session, [], [30])

    assert session.finished_races == [first, second, third]


def test_history_is_not_lost_when_a_new_race_starts():
    session = RaceSession()
    first = run_race(session, [], [10])

    StartRace(session).execute()

    assert session.finished_races == [first]
    assert session.active_race is not None


def test_cannot_start_a_race_while_another_is_active():
    session = RaceSession()
    first = StartRace(session).execute()

    second = StartRace(session).execute()

    assert second is None
    assert session.active_race is first


def test_finishing_twice_does_not_duplicate_the_history():
    session = RaceSession()
    run_race(session, [], [10])

    result = FinishRace(session).execute()

    assert result is None
    assert len(session.finished_races) == 1


def test_many_consecutive_races_leave_the_session_ready():
    session = RaceSession()

    for _ in range(5):
        run_race(session, [RaceStatus.MOVING, RaceStatus.STOPPED], [5, 5, 5])

    assert len(session.finished_races) == 5
    assert session.active_race is None
