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