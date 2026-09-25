from domain.race import Race


class StartRace:
    def __init__(self):
        self.active_race = None
    
    def execute(self):
        if self.active_race is not None:
            print("Una carrera ya está en curso")
            return None
        
        self.active_race = Race()
        print("Empieza la carrera")
        return self.active_race