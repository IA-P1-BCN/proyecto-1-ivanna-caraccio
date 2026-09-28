import json
from datetime import datetime
from pathlib import Path

from domain.race_record import RaceRecord


class RaceHistoryRepository:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def save(self, record):
        records = self.get_all()
        records.append(record)
        self._write_all(records)

    def get_all(self):
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [self._from_dict(item) for item in data]
        except (ValueError, KeyError, TypeError):
            raise ValueError(
                f"The history file is corrupted: {self.file_path}")

    def get_by_date(self, day):
        return [r for r in self.get_all() if r.start_time.date() == day]

    def _write_all(self, records):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [self._to_dict(record) for record in records]

        temp_path = self.file_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        temp_path.replace(self.file_path)

    @staticmethod
    def _to_dict(record):
        return {
            "start_time": record.start_time.isoformat(),
            "end_time": record.end_time.isoformat(),
            "duration_seconds": record.duration_seconds,
            "total_amount": record.total_amount,
        }

    @staticmethod
    def _from_dict(data):
        return RaceRecord(
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            duration_seconds=data["duration_seconds"],
            total_amount=data["total_amount"],
        )
