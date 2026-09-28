class FinishRace:
    def __init__(self, session, repository):
        self.session = session
        self.repository = repository

    def execute(self):
        race = self.session.active_race

        if race is None:
            print("No hay ninguna carrera por terminar.")
            return None

        race.finish()
        self.session.active_race = None
        
        try:
            self.repository.save(race.to_record())
        except (OSError, ValueError):
            print("Advertencia: No se ha podido registrar la carrera.")

        
        return race
