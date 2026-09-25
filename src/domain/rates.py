from .race_status import RaceStatus


RATE_PER_SECOND = {
    RaceStatus.STOPPED: 0.02,
    RaceStatus.MOVING: 0.05,
}
