from pathlib import Path

from infrastructure.race_history_repository import RaceHistoryRepository
from interfaces.cli import Cli

HISTORY_FILE = Path(__file__).resolve().parent.parent / \
    "data" / "race_history.json"


if __name__ == "__main__":
    repository = RaceHistoryRepository(HISTORY_FILE)
    Cli(repository).run()
