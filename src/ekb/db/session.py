from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ekb.core.config import Settings


def build_engine(settings: Settings) -> Engine:
    connect_args = (
        {"check_same_thread": False}
        if settings.database.url.startswith("sqlite")
        else {}
    )
    return create_engine(settings.database.url, connect_args=connect_args)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
