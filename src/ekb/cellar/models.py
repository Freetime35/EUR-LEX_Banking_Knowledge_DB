from dataclasses import dataclass


@dataclass(frozen=True)
class TreeNotice:
    """Minimal representation of a Cellar Tree Notice."""

    work_uri: str
    same_as: tuple[str, ...]