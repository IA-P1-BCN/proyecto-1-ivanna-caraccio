from domain.race import Race


class StartRace:
    def __init__(self, session):
        self.session = session
    
    def execute(self):
        if self.session.active_race is not None:
            print("Una carrera ya está en curso")
            return None
        
        self.session.active_race = Race()
        print("Empieza la carrera")
        return self.session.active_race