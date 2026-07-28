from rdflib import Graph, URIRef

from ekb.extractors.relation import LegalRelationExtractor
from ekb.models.relation import LegalRelation, RelationType


def test_extracts_amends_relation() -> None:
    graph = Graph()

    source = URIRef(
        "http://publications.europa.eu/resource/celex/32022R2554"
    )
    target = URIRef(
        "http://publications.europa.eu/resource/celex/32013R0575"
    )
    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "resource_legal_amends_resource_legal"
    )

    graph.add((source, predicate, target))

    relations = LegalRelationExtractor().extract(graph)

    assert relations == [
        LegalRelation(
            source_celex="32022R2554",
            relation=RelationType.AMENDS,
            target_celex="32013R0575",
        )
    ]


def test_ignores_non_celex_resources() -> None:
    graph = Graph()

    source = URIRef(
        "http://publications.europa.eu/resource/cellar/source"
    )
    target = URIRef(
        "http://publications.europa.eu/resource/celex/32013R0575"
    )
    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "resource_legal_amends_resource_legal"
    )

    graph.add((source, predicate, target))

    relations = LegalRelationExtractor().extract(graph)

    assert relations == []
