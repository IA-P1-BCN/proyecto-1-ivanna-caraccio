from domain.race_status import RaceStatus

class ChangeRaceStatus:
    def __init__(self, session):
        self.session = session
    
    def execute(self, new_status):
        race = self.session.active_race

        if race is None:
            print("No hay carrera activa. Empieza una primero.")
            return None

        if race.status == new_status:
            return race

        race.change_status(new_status)
        return race
