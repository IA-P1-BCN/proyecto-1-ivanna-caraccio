from domain.race_status import RaceStatus

class ChangeRaceStatus:
    def __init__(self, session):
        self.session = session
    
    def execute(self):
        race = self.session.active_race

        if race is None:
            print("No hay carrera activa. Empieza una primero.")
            return None

        if race.status == RaceStatus.STOPPED:
            new_status = RaceStatus.MOVING
        else:
            new_status = RaceStatus.STOPPED

        race.change_status(new_status)
        print(f"Estado: {new_status.value}")
        return race
