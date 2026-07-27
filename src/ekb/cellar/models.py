from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    """Minimal representation of a Cellar Expression."""

    uri: str
    language: str | None


@dataclass(frozen=True)
class Item:
    """Minimal representation of a Cellar Item."""

    uri: str
    identifier: str
    filename: str
    size: int
    order: int
    label: str
    composition_level: int


@dataclass(frozen=True)
class Manifestation:
    """Minimal representation of a Cellar Manifestation."""

    uri: str
    same_as: tuple[str, ...]
    expression_uri: str
    media_type: str
    items: tuple[Item, ...]


@dataclass(frozen=True)
class TreeNotice:
    """Minimal representation of a Cellar Tree Notice."""

    work_uri: str
    celex_id: str
    resource_legal_type: str
    same_as: tuple[str, ...]
    expressions: tuple[Expression, ...]
    manifestations: tuple[Manifestation, ...]