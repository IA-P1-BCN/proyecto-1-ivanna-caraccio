import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "taximeter.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_BYTES = 1_000_000
BACKUP_COUNT = 5
_MARKER = "taximeter-file-handler"
REDACTED = "***"
_sensitive_values = set()


def register_sensitive_value(value):
    if value:
        _sensitive_values.add(value)


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        masked = message
        for value in sorted(_sensitive_values, key=len, reverse=True):
            masked = masked.replace(value, REDACTED)

        if masked != message:
            record.msg = masked
            record.args = ()

        return True


def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    if any(getattr(handler, "_marker", None) == _MARKER
           for handler in root.handlers):
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    handler._marker = _MARKER
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    handler.addFilter(SensitiveDataFilter())

    root.addHandler(handler)


def get_logger(name):
    return logging.getLogger(name)
