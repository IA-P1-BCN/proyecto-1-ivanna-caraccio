import sys
from pathlib import Path

from infrastructure.logging_config import get_logger, setup_logging
from infrastructure.race_history_repository import RaceHistoryRepository
from interfaces.cli import Cli

HISTORY_FILE = Path(__file__).resolve().parent.parent / \
    "data" / "race_history.json"

logger = get_logger(__name__)


def main():
    setup_logging()
    logger.info("Application started")

    repository = RaceHistoryRepository(HISTORY_FILE)

    try:
        Cli(repository).run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by the user")
    except Exception:
        logger.exception("Unhandled exception")
        print("Se ha producido un error inesperado. "
              "Consulta el fichero de log para más detalles.")
        return 1
    finally:
        logger.info("Application closed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
