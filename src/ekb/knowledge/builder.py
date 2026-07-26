"""Knowledge graph construction."""

from rdflib import Graph

from ekb.extractors.document import DocumentExtractor
from ekb.knowledge.graph import KnowledgeGraph


class KnowledgeGraphBuilder:
    """Build a domain knowledge graph from an RDF graph."""

    def __init__(
        self,
        document_extractor: DocumentExtractor | None = None,
    ) -> None:
        self._document_extractor = (
            document_extractor or DocumentExtractor()
        )

    def build(self, graph: Graph) -> KnowledgeGraph:
        """Build a knowledge graph from RDF data."""

        documents = self._document_extractor.extract(graph)

        return KnowledgeGraph(
            rdf_graph=graph,
            documents=documents,
        )