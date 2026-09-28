import msvcrt
import time

from application.race_session import RaceSession
from application.start_race import StartRace
from application.change_race_status import ChangeRaceStatus
from domain.race_status import RaceStatus

ARROW_PREFIXES = ("\x00", "\xe0")
CODE_UP = "H"
CODE_DOWN = "P"

def read_key():
    if not msvcrt.kbhit():
        return None

    key = msvcrt.getwch()

    if key in ARROW_PREFIXES:
        code = msvcrt.getwch()
        if code == CODE_UP:
            return "UP"
        if code == CODE_DOWN:
            return "DOWN"
        return None

    return key.lower()

class Cli:
    def __init__(self):
        self.session = None
        self.change_race_status = None
    
    def run(self):
        while True:
            print("\n=== TAXIMETER ===")
            print("1. Iniciar carrera")
            print("2. Salir")
            choice = input("Elige una opción: ").strip()

            if choice == "1":
                self._start_race_flow()
            elif choice == "2":
                print("¡Adiós!")
                break
            else:
                print("Opción no válida.")

    def _start_race_flow(self):
        self.session = RaceSession()
        start_race = StartRace(self.session)
        self.change_race_status = ChangeRaceStatus(self.session)

        start_race.execute()
        self._run_race_screen()

    def _run_race_screen(self):
        print("Flecha arriba = en movimiento | Flecha abajo = parado | Q = salir\n")

        last_refresh = 0

        while True:
            key = read_key()

            if key == "q":
                print()
                break

            key_changed_status = False
            if key == "UP":
                self._change_status(RaceStatus.MOVING)
                key_changed_status = True
            elif key == "DOWN":
                self._change_status(RaceStatus.STOPPED)
                key_changed_status = True

            now = time.time()
            if now - last_refresh >= 1 or key_changed_status:
                self._draw_status()
                last_refresh = now

            time.sleep(0.05)

    def _change_status(self, new_status):
        print("\r" + " " * 60 + "\r", end="")
        self.change_race_status.execute(new_status)

    def _draw_status(self):
        race = self.session.active_race
        amount = race.get_current_amount()
        line = f"Estado: {race.status.value:<8} | Cantidad: {amount:.2f} €"
        print("\r" + line + " " * 10, end="", flush=True)
