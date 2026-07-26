from pathlib import Path

from ekb.core.config import Settings
from ekb.services.database import init_database, seed_collections


def test_database_initialization(tmp_path: Path) -> None:
    settings = Settings(database={"url": f"sqlite:///{tmp_path / 'test.sqlite3'}"})
    tables = init_database(settings)
    assert {"documents", "identifiers", "collections", "sync_runs"}.issubset(tables)
    assert seed_collections(settings) == 8
    assert seed_collections(settings) == 0
