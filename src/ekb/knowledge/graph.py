from dataclasses import dataclass, field
from typing import Any

from rdflib import Graph


@dataclass(slots=True)
class KnowledgeGraph:
    rdf_graph: Graph

    documents: list[Any] = field(default_factory=list)
    relations: list[Any] = field(default_factory=list)

    eurovoc_concepts: list[Any] = field(default_factory=list)
    procedures: list[Any] = field(default_factory=list)
    events: list[Any] = field(default_factory=list)

    official_journals: list[Any] = field(default_factory=list)

    expressions: list[Any] = field(default_factory=list)
    manifestations: list[Any] = field(default_factory=list)