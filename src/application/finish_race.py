class FinishRace:
    """
    Use case: finishes the active race.
    """

    def __init__(self, session):
        self.session = session

    def execute(self):
        race = self.session.active_race

        if race is None:
            print("No hay ninguna carrera por terminar.")
            return None

        race.finish()
        self.session.active_race = None  # free the session for a new race
        return race
