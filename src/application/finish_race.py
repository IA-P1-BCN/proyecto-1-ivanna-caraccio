class FinishRace:
    def __init__(self, session):
        self.session = session

    def execute(self):
        race = self.session.active_race

        if race is None:
            print("No hay ninguna carrera por terminar.")
            return None

        race.finish()
        self.session.finished_races.append(race)
        self.session.active_race = None
        return race
