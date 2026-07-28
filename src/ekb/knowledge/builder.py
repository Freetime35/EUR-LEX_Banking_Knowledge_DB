from rdflib import Graph

from ekb.extractors.document import DocumentExtractor
from ekb.extractors.metadata import MetadataExtractor
from ekb.extractors.relation import LegalRelationExtractor
from ekb.knowledge.graph import KnowledgeGraph


class KnowledgeGraphBuilder:

    def __init__(
        self,
        document_extractor: DocumentExtractor | None = None,
        metadata_extractor: MetadataExtractor | None = None,
        relation_extractor: LegalRelationExtractor | None = None,
    ) -> None:
        self._document_extractor = (
            document_extractor or DocumentExtractor()
        )
        self._metadata_extractor = (
            metadata_extractor or MetadataExtractor()
        )
        self._relation_extractor = (
            relation_extractor or LegalRelationExtractor()
        )

    def build(self, graph: Graph) -> KnowledgeGraph:
        documents = self._document_extractor.extract(graph)

        for document in documents:
            document.metadata = self._metadata_extractor.extract(
                graph,
                document.uri,
            )

        relations = self._relation_extractor.extract(graph)

        return KnowledgeGraph(
            rdf_graph=graph,
            documents=documents,
            relations=relations,
        )
