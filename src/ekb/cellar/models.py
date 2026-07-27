from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    uri: str
    language: str | None


@dataclass(frozen=True)
class Item:
    uri: str
    identifier: str
    filename: str
    size: int
    order: int
    label: str
    composition_level: int


@dataclass(frozen=True)
class Manifestation:
    uri: str
    same_as: tuple[str, ...]
    expression_uri: str
    media_type: str
    items: tuple[Item, ...]


@dataclass(frozen=True)
class TreeNotice:
    work_uri: str
    celex_id: str
    resource_legal_type: str
    document_date: str
    document_id: str
    legal_event: str
    year: str
    treaty_basis: str
    subject_matters: tuple[str, ...]
    creators: tuple[str, ...]
    same_as: tuple[str, ...]
    expressions: tuple[Expression, ...]
    manifestations: tuple[Manifestation, ...]
