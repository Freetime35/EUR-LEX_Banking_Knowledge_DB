"""Document extraction from RDF graphs."""

from rdflib import RDF, Graph, URIRef
from rdflib.namespace import Namespace

from ekb.models.document import Document

CDM = Namespace("http://publications.europa.eu/ontology/cdm#")


class DocumentExtractor:
    """Extract legal documents from an RDF graph."""

    def extract(self, graph: Graph) -> list[Document]:
        """Return every RDF resource typed as a CDM legal resource."""

        document_uris = {
            subject
            for subject in graph.subjects(
                predicate=RDF.type,
                object=CDM.resource_legal,
            )
            if isinstance(subject, URIRef)
        }

        return [
            Document(uri=uri)
            for uri in sorted(document_uris, key=str)
        ]