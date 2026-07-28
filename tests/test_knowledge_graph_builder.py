from rdflib import RDF, Graph, URIRef
from rdflib.namespace import OWL

from ekb.extractors.document import CDM
from ekb.extractors.metadata import MetadataExtractor
from ekb.knowledge.builder import KnowledgeGraphBuilder
from ekb.models.relation import LegalRelation, RelationType


def test_build_returns_knowledge_graph() -> None:
    graph = Graph()

    kg = KnowledgeGraphBuilder().build(graph)

    assert kg.rdf_graph is graph


def test_build_initializes_empty_collections() -> None:
    kg = KnowledgeGraphBuilder().build(Graph())

    assert kg.documents == []
    assert kg.relations == []
    assert kg.eurovoc_concepts == []
    assert kg.procedures == []
    assert kg.events == []
    assert kg.official_journals == []
    assert kg.expressions == []
    assert kg.manifestations == []


def test_build_extracts_documents() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001"
    )
    graph.add((document_uri, RDF.type, CDM.resource_legal))

    knowledge_graph = KnowledgeGraphBuilder().build(graph)

    assert knowledge_graph.rdf_graph is graph
    assert len(knowledge_graph.documents) == 1
    assert knowledge_graph.documents[0].uri == document_uri


def test_build_extracts_document_metadata() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "52020DC0067"
    )

    graph.add((document_uri, RDF.type, CDM.resource_legal))
    graph.add((document_uri, OWL.sameAs, celex_uri))

    knowledge_graph = KnowledgeGraphBuilder().build(graph)

    assert len(knowledge_graph.documents) == 1
    assert knowledge_graph.documents[0].metadata is not None
    assert (
        knowledge_graph.documents[0].metadata.celex
        == "52020DC0067"
    )

def test_extracts_celex_through_shared_cellar_alias() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((cellar_uri, OWL.sameAs, document_uri))
    graph.add((cellar_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32022R2554"

def test_returns_none_when_cellar_alias_has_no_celex() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/test"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    eli_uri = URIRef(
        "http://publications.europa.eu/resource/eli/"
        "reg/2022/2554/oj"
    )

    graph.add((cellar_uri, OWL.sameAs, document_uri))
    graph.add((cellar_uri, OWL.sameAs, eli_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is None

def test_build_extracts_legal_relations() -> None:
    graph = Graph()

    source_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )
    target_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32013R0575"
    )
    predicate = URIRef(
        "http://publications.europa.eu/ontology/cdm#"
        "resource_legal_amends_resource_legal"
    )

    graph.add((source_uri, predicate, target_uri))

    knowledge_graph = KnowledgeGraphBuilder().build(graph)

    assert knowledge_graph.relations == [
        LegalRelation(
            source_celex="32022R2554",
            relation=RelationType.AMENDS,
            target_celex="32013R0575",
        )
    ]
