from datetime import date


class GetTodayHistory:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, day=None):
        if day is None:
            day = date.today()

        records = self.repository.get_by_date(day)
        return records, self.calculate_total(records)

    @staticmethod
    def calculate_total(records):
        total = sum(record.total_amount for record in records)
        return round(total, 2)
