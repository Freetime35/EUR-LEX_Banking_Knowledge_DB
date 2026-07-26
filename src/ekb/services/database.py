from __future__ import annotations

from sqlalchemy import inspect, select

from ekb.core.config import Settings
from ekb.db.base import Base
from ekb.db.models import Collection
from ekb.db.session import build_engine, build_session_factory


DEFAULT_COLLECTIONS = (
    ("BANKING", "Banking", "Réglementation prudentielle et supervision bancaire"),
    ("CAPITAL_REQUIREMENTS", "Capital Requirements", "CRR, CRD et actes associés"),
    ("BANK_RECOVERY", "Bank Recovery & Resolution", "BRRD, SRMR et résolution"),
    ("FINANCIAL_MARKETS", "Financial Markets", "MiFID, MiFIR, EMIR, CSDR, MAR"),
    ("PAYMENTS", "Payments", "Paiements et monnaie électronique"),
    ("DIGITAL_FINANCE", "Digital Finance", "DORA, MiCA et finance numérique"),
    ("AML", "AML/CFT", "Lutte contre le blanchiment et financement du terrorisme"),
    ("SUSTAINABLE_FINANCE", "Sustainable Finance", "SFDR, taxonomie et ESG"),
)


def init_database(settings: Settings) -> list[str]:
    settings.ensure_directories()
    engine = build_engine(settings)
    Base.metadata.create_all(engine)
    return inspect(engine).get_table_names()


def seed_collections(settings: Settings) -> int:
    engine = build_engine(settings)
    factory = build_session_factory(engine)
    created = 0
    with factory() as session:
        for code, name, description in DEFAULT_COLLECTIONS:
            existing = session.scalar(select(Collection).where(Collection.code == code))
            if existing is None:
                session.add(Collection(code=code, name=name, description=description))
                created += 1
        session.commit()
    return created
