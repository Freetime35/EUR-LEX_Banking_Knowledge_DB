"""Extract legal relationships from an RDF graph."""

from urllib.parse import unquote

from rdflib import Graph, URIRef

from ekb.cdm import (
    RESOURCE_LEGAL_AMENDS,
    RESOURCE_LEGAL_BASED_ON,
    RESOURCE_LEGAL_REPEALS,
    WORK_CITES,
)
from ekb.models.relation import LegalRelation, RelationType

CELEX_URI_PREFIX = (
    "http://publications.europa.eu/resource/celex/"
)

RELATION_MAPPING = {
    RESOURCE_LEGAL_AMENDS: RelationType.AMENDS,
    RESOURCE_LEGAL_REPEALS: RelationType.REPEALS,
    WORK_CITES: RelationType.CITES,
    RESOURCE_LEGAL_BASED_ON: RelationType.BASED_ON,
}


class LegalRelationExtractor:
    """Extract legal relationships between CELEX resources."""

    def extract(self, graph: Graph) -> list[LegalRelation]:
        relations: list[LegalRelation] = []

        for predicate, relation_type in RELATION_MAPPING.items():
            for source_uri, target_uri in graph.subject_objects(predicate):
                source_celex = self._celex_from_uri(source_uri)
                target_celex = self._celex_from_uri(target_uri)

                if source_celex is None or target_celex is None:
                    continue

                relations.append(
                    LegalRelation(
                        source_celex=source_celex,
                        relation=relation_type,
                        target_celex=target_celex,
                    )
                )

        return relations

    def _celex_from_uri(self, uri: object) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(CELEX_URI_PREFIX):
            return None

        encoded_celex = uri_value.removeprefix(
            CELEX_URI_PREFIX
        )

        return unquote(encoded_celex)
