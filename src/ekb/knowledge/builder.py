from rdflib import Graph

from ekb.extractors.document import DocumentExtractor
from ekb.extractors.metadata import MetadataExtractor
from ekb.knowledge.graph import KnowledgeGraph


class KnowledgeGraphBuilder:

    def __init__(
        self,
        document_extractor: DocumentExtractor | None = None,
        metadata_extractor: MetadataExtractor | None = None,
    ) -> None:
        self._document_extractor = (
            document_extractor or DocumentExtractor()
        )
        self._metadata_extractor = (
            metadata_extractor or MetadataExtractor()
        )

    def build(self, graph: Graph) -> KnowledgeGraph:
        documents = self._document_extractor.extract(graph)

        for document in documents:
            document.metadata = self._metadata_extractor.extract(
                graph,
                document.uri,
            )

        return KnowledgeGraph(
            rdf_graph=graph,
            documents=documents,
        )