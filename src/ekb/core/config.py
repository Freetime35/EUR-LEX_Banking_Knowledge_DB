from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource


class AppSettings(BaseModel):
    environment: Literal["development", "test", "production"] = "development"
    log_level: str = "INFO"


class DatabaseSettings(BaseModel):
    url: str = "sqlite:///data/database/ekb.sqlite3"


class StorageSettings(BaseModel):
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    exports_dir: Path = Path("data/exports")
    cache_dir: Path = Path("data/cache")


class HttpSettings(BaseModel):
    timeout_seconds: float = Field(default=60, gt=0)
    max_retries: int = Field(default=5, ge=0)
    rate_limit_per_second: float = Field(default=1.0, gt=0)
    user_agent: str = "EURLEX-Knowledge-DB/0.1"


class CollectionSettings(BaseModel):
    default_languages: list[str] = ["fr", "en"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="config/settings.toml",
        env_prefix="EKB_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    storage: StorageSettings = StorageSettings()
    http: HttpSettings = HttpSettings()
    collection: CollectionSettings = CollectionSettings()

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):  # type: ignore[no-untyped-def]
        return (TomlConfigSettingsSource(settings_cls), kwargs["env_settings"])

    def ensure_directories(self) -> None:
        for path in (
            self.storage.raw_dir,
            self.storage.processed_dir,
            self.storage.exports_dir,
            self.storage.cache_dir,
            Path("data/database"),
            Path("logs"),
        ):
            path.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
