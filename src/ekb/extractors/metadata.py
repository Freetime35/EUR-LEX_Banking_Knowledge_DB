from urllib.parse import unquote

from rdflib import Graph, URIRef
from rdflib.namespace import OWL

from ekb.models.document import DocumentMetadata


CELEX_URI_PREFIX = (
    "http://publications.europa.eu/resource/celex/"
)


class MetadataExtractor:

    def extract(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> DocumentMetadata | None:
        celex = self._extract_celex(graph, document_uri)

        if celex is None:
            return None

        return DocumentMetadata(celex=celex)

    def _extract_celex(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> str | None:
        direct_celex = self._celex_from_uri(document_uri)

        if direct_celex is not None:
            return direct_celex

        for same_as in graph.objects(document_uri, OWL.sameAs):
            celex = self._celex_from_uri(same_as)

            if celex is not None:
                return celex

        for alias_subject in graph.subjects(
            OWL.sameAs,
            document_uri,
        ):
            for same_as in graph.objects(
                alias_subject,
                OWL.sameAs,
            ):
                celex = self._celex_from_uri(same_as)

                if celex is not None:
                    return celex

        return None

    def _celex_from_uri(
        self,
        uri: object,
    ) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(CELEX_URI_PREFIX):
            return None

        encoded_celex = uri_value.removeprefix(
            CELEX_URI_PREFIX
        )

        return unquote(encoded_celex)