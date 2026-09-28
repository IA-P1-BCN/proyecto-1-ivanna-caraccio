import os
import sys

import pytest

CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")

sys.path.insert(0, os.path.abspath(SRC_DIR))


@pytest.fixture
def repository(tmp_path):
    from infrastructure.race_history_repository import RaceHistoryRepository

    return RaceHistoryRepository(tmp_path / "race_history.json")
