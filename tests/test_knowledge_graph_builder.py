from rdflib import Graph

from ekb.knowledge.builder import KnowledgeGraphBuilder


def test_build_returns_knowledge_graph():
    graph = Graph()

    kg = KnowledgeGraphBuilder().build(graph)

    assert kg.rdf_graph is graph


def test_build_initializes_empty_collections():
    kg = KnowledgeGraphBuilder().build(Graph())

    assert kg.documents == []
    assert kg.relations == []
    assert kg.eurovoc_concepts == []
    assert kg.procedures == []
    assert kg.events == []
    assert kg.official_journals == []
    assert kg.expressions == []
    assert kg.manifestations == []
from rdflib import Graph, RDF, URIRef

from ekb.extractors.document import CDM
from ekb.knowledge.builder import KnowledgeGraphBuilder


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