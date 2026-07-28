from dataclasses import dataclass
from enum import StrEnum


class RelationType(StrEnum):
    AMENDS = "amends"
    REPEALS = "repeals"
    CITES = "cites"
    BASED_ON = "based_on"


@dataclass(frozen=True, slots=True)
class LegalRelation:
    source_celex: str
    relation: RelationType
    target_celex: str