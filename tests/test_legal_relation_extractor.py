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


def test_extracts_repeals_relation() -> None:
    graph = Graph()

    source = URIRef(
        "http://publications.europa.eu/resource/celex/32022R2554"
    )
    target = URIRef(
        "http://publications.europa.eu/resource/celex/32013R0575"
    )

    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "resource_legal_repeals_resource_legal"
    )

    graph.add((source, predicate, target))

    relations = LegalRelationExtractor().extract(graph)

    assert relations == [
        LegalRelation(
            source_celex="32022R2554",
            relation=RelationType.REPEALS,
            target_celex="32013R0575",
        )
    ]


def test_extracts_cites_relation() -> None:
    graph = Graph()

    source = URIRef(
        "http://publications.europa.eu/resource/celex/32022R2554"
    )
    target = URIRef(
        "http://publications.europa.eu/resource/celex/32013R0575"
    )
    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "work_cites_work"
    )

    graph.add((source, predicate, target))

    relations = LegalRelationExtractor().extract(graph)

    assert relations == [
        LegalRelation(
            source_celex="32022R2554",
            relation=RelationType.CITES,
            target_celex="32013R0575",
        )
    ]


def test_extracts_based_on_relation() -> None:
    graph = Graph()

    source = URIRef(
        "http://publications.europa.eu/resource/celex/32022R2554"
    )
    target = URIRef(
        "http://publications.europa.eu/resource/celex/12012E/TXT"
    )
    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "resource_legal_based_on_resource_legal"
    )

    graph.add((source, predicate, target))

    relations = LegalRelationExtractor().extract(graph)

    assert relations == [
        LegalRelation(
            source_celex="32022R2554",
            relation=RelationType.BASED_ON,
            target_celex="12012E/TXT",
        )
    ]
