"""Shared connector models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class DocumentMetadata:
    """Metadata describing a legal document."""

    celex: str
    title: str | None = None
    eli: str | None = None
    cellar_id: str | None = None

    document_type: str | None = None

    date_document: date | None = None
    date_publication: date | None = None

    languages: list[str] = field(default_factory=list)