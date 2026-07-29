"""Document domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from rdflib import URIRef


@dataclass(slots=True)
class Document:
    """A legal document identified in an RDF graph."""

    uri: URIRef
    metadata: DocumentMetadata | None = None


@dataclass(slots=True)
class DocumentMetadata:
    """Metadata describing a legal document."""

    celex: str

    # Preferred title (ENG → FRA → first available)
    title: str | None = None

    # All localized titles keyed by language code
    titles: dict[str, str] = field(default_factory=dict)

    eli: str | None = None
    cellar_id: str | None = None

    document_type: str | None = None
    legal_type: str | None = None
    rdf_types: tuple[str, ...] = ()

    date_document: date | None = None
    date_publication: date | None = None

    languages: list[str] = field(default_factory=list)
    
    eurovoc_concepts: tuple[str, ...] = ()

    is_about: tuple[str, ...] = ()
