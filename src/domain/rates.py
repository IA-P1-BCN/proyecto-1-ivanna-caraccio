from .race_status import RaceStatus

RATE_PER_SECOND = {
    RaceStatus.STOPPED: 0.02,
    RaceStatus.MOVING: 0.05,
}


class Rates:
    def __init__(self, stopped, moving):
        self._stopped = stopped
        self._moving = moving

    @property
    def stopped(self):
        return self._stopped

    @property
    def moving(self):
        return self._moving

    def for_status(self, status):
        if status == RaceStatus.STOPPED:
            return self._stopped

        if status == RaceStatus.MOVING:
            return self._moving

        raise ValueError(f"Estado desconocido: {status}")


DEFAULT_RATES = Rates(stopped=0.02, moving=0.05)
