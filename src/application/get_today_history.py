from datetime import date

from infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class GetTodayHistory:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, day=None):
        if day is None:
            day = date.today()

        try:
            records = self.repository.get_by_date(day)
        except ValueError:
            logger.warning("History for %s could not be read", day,
                           exc_info=True)
            raise

        total = self.calculate_total(records)
        logger.info("History queried for %s: %s races, total=%.2f",
                    day, len(records), total)
        return records, total

    @staticmethod
    def calculate_total(records):
        total = sum(record.total_amount for record in records)
        return round(total, 2)
