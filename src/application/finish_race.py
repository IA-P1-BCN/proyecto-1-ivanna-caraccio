from infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class FinishRace:
    def __init__(self, session, repository):
        self.session = session
        self.repository = repository

    def execute(self):
        race = self.session.active_race

        if race is None:
            logger.warning("Race not finished: no active race")
            print("No hay ninguna carrera por terminar.")
            return None

        race.finish()
        self.session.active_race = None
        logger.info("Race finished: start=%s end=%s duration=%.2fs amount=%.2f",
                    race.start_time, race.end_time,
                    race.get_duration_seconds(), race.get_current_amount())

        try:
            self.repository.save(race.to_record())
        except (OSError, ValueError):
            logger.error("Race record could not be saved", exc_info=True)
            print("Advertencia: No se ha podido registrar la carrera.")

        return race
