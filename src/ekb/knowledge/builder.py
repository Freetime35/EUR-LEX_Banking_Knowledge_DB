from rdflib import Graph

from ekb.knowledge.graph import KnowledgeGraph


class KnowledgeGraphBuilder:
    def build(self, graph: Graph) -> KnowledgeGraph:
        return KnowledgeGraph(rdf_graph=graph)