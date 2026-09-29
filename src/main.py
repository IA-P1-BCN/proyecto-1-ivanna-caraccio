import sys
from pathlib import Path

from application.validate_access import ValidateAccess
from infrastructure.auth_config import AuthConfig
from infrastructure.config_error import ConfigError
from infrastructure.logging_config import get_logger, setup_logging
from infrastructure.race_history_repository import RaceHistoryRepository
from infrastructure.rates_config import RatesConfig
from interfaces.cli import Cli

HISTORY_FILE = Path(__file__).resolve().parent.parent / \
    "data" / "race_history.json"
RATES_FILE = Path(__file__).resolve().parent.parent / \
    "config" / "rates.json"
AUTH_FILE = Path(__file__).resolve().parent.parent / \
    "config" / "auth.json"

logger = get_logger(__name__)


def main():
    setup_logging()
    logger.info("Application started")

    try:
        rates = RatesConfig(RATES_FILE).load()
        password_hash = AuthConfig(AUTH_FILE).load()
    except ConfigError as error:
        logger.error("Configuration error: %s", error)
        logger.info("Application closed")
        print(f"Error de configuración: {error.user_message}")
        print("Corrige el fichero de configuración y vuelve a intentarlo.")
        return 1

    logger.info("Rates loaded: stopped=%s moving=%s",
                rates.stopped, rates.moving)
    logger.info("Password hash loaded")

    repository = RaceHistoryRepository(HISTORY_FILE)
    validate_access = ValidateAccess(password_hash)

    try:
        if "--gui" in sys.argv[1:]:
            from interfaces.gui import TaxiGui

            TaxiGui(repository, rates, validate_access).run()
        else:
            Cli(repository, rates, validate_access).run()
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
