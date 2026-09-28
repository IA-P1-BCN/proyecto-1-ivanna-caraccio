from domain.race import Race
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class StartRace:
    def __init__(self, session, rates=None):
        self.session = session
        self.rates = rates

    def execute(self):
        if self.session.active_race is not None:
            logger.warning("Race not started: another race is already active")
            print("Una carrera ya está en curso")
            return None

        self.session.active_race = Race(self.rates)
        logger.info("Race started at %s (status: %s)",
                    self.session.active_race.start_time,
                    self.session.active_race.status.value)
        print("Empieza la carrera")
        return self.session.active_race
