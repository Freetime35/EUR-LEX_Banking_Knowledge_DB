"""Extract legal relationships from an RDF graph."""

from urllib.parse import unquote

from rdflib import Graph, URIRef

from ekb.models.relation import LegalRelation, RelationType

CELEX_URI_PREFIX = (
    "http://publications.europa.eu/resource/celex/"
)

CDM_URI_PREFIX = (
    "http://publications.europa.eu/ontology/cdm#"
)

RELATION_MAPPING = {
    URIRef(
        f"{CDM_URI_PREFIX}resource_legal_amends_resource_legal"
    ): RelationType.AMENDS,
    URIRef(
        f"{CDM_URI_PREFIX}resource_legal_repeals_resource_legal"
    ): RelationType.REPEALS,
    URIRef(
        f"{CDM_URI_PREFIX}work_cites_work"
    ): RelationType.CITES,
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
