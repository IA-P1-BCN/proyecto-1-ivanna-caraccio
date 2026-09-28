from infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class ChangeRaceStatus:
    def __init__(self, session):
        self.session = session

    def execute(self, new_status):
        race = self.session.active_race

        if race is None:
            logger.warning("Status not changed to '%s': no active race",
                           new_status.value)
            print("No hay carrera activa. Empieza una primero.")
            return None

        previous_status = race.status

        if race.status == new_status:
            logger.debug("Status unchanged: race is already '%s'",
                         new_status.value)
            return race

        race.change_status(new_status)
        logger.info("Race status changed: %s -> %s",
                    previous_status.value, new_status.value)
        return race
