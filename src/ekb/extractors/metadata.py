from urllib.parse import unquote

from rdflib import Graph, URIRef
from rdflib.namespace import OWL

from ekb.models.document import DocumentMetadata


CELEX_URI_PREFIX = (
    "http://publications.europa.eu/resource/celex/"
)

ELI_URI_PREFIX = (
    "http://publications.europa.eu/resource/eli/"
)

CELLAR_URI_PREFIX = (
    "http://publications.europa.eu/resource/cellar/"
)


class MetadataExtractor:

    def extract(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> DocumentMetadata | None:
        celex = self._extract_celex(
            graph,
            document_uri,
        )

        if celex is None:
            return None

        eli = self._extract_eli(
            graph,
            document_uri,
        )

        cellar_id = self._extract_cellar_id(
            graph,
            document_uri,
        )

        return DocumentMetadata(
            celex=celex,
            eli=eli,
            cellar_id=cellar_id,
        )

    def _extract_celex(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> str | None:
        direct_celex = self._celex_from_uri(
            document_uri
        )

        if direct_celex is not None:
            return direct_celex

        for same_as in graph.objects(
            document_uri,
            OWL.sameAs,
        ):
            celex = self._celex_from_uri(
                same_as
            )

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
                celex = self._celex_from_uri(
                    same_as
                )

                if celex is not None:
                    return celex

        return None

    def _extract_eli(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> str | None:
        direct_eli = self._eli_from_uri(
            document_uri
        )

        if direct_eli is not None:
            return direct_eli

        for same_as in graph.objects(
            document_uri,
            OWL.sameAs,
        ):
            eli = self._eli_from_uri(
                same_as
            )

            if eli is not None:
                return eli

        for alias_subject in graph.subjects(
            OWL.sameAs,
            document_uri,
        ):
            for same_as in graph.objects(
                alias_subject,
                OWL.sameAs,
            ):
                eli = self._eli_from_uri(
                    same_as
                )

                if eli is not None:
                    return eli

        return None

    def _extract_cellar_id(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> str | None:
        direct_cellar_id = self._cellar_id_from_uri(
            document_uri
        )

        if direct_cellar_id is not None:
            return direct_cellar_id

        for same_as in graph.objects(
            document_uri,
            OWL.sameAs,
        ):
            cellar_id = self._cellar_id_from_uri(
                same_as
            )

            if cellar_id is not None:
                return cellar_id

        for alias_subject in graph.subjects(
            OWL.sameAs,
            document_uri,
        ):
            cellar_id = self._cellar_id_from_uri(
                alias_subject
            )

            if cellar_id is not None:
                return cellar_id

            for same_as in graph.objects(
                alias_subject,
                OWL.sameAs,
            ):
                cellar_id = self._cellar_id_from_uri(
                    same_as
                )

                if cellar_id is not None:
                    return cellar_id

        return None

    def _celex_from_uri(
        self,
        uri: object,
    ) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(
            CELEX_URI_PREFIX
        ):
            return None

        encoded_celex = uri_value.removeprefix(
            CELEX_URI_PREFIX
        )

        return unquote(encoded_celex)

    def _eli_from_uri(
        self,
        uri: object,
    ) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(
            ELI_URI_PREFIX
        ):
            return None

        return uri_value

    def _cellar_id_from_uri(
        self,
        uri: object,
    ) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(
            CELLAR_URI_PREFIX
        ):
            return None

        encoded_cellar_id = uri_value.removeprefix(
            CELLAR_URI_PREFIX
        )

        return unquote(encoded_cellar_id)