"""Extract document metadata from an RDF graph."""

from urllib.parse import unquote

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL

from ekb.models.document import DocumentMetadata

from ekb.cdm import RESOURCE_LEGAL_TYPE

from rdflib.namespace import RDF

CELEX_URI_PREFIX = (
    "http://publications.europa.eu/resource/celex/"
)

ELI_URI_PREFIX = (
    "http://publications.europa.eu/resource/eli/"
)

CELLAR_URI_PREFIX = (
    "http://publications.europa.eu/resource/cellar/"
)

CDM_URI_PREFIX = (
    "http://publications.europa.eu/ontology/cdm#"
)

LANGUAGE_URI_PREFIX = (
    "http://publications.europa.eu/resource/"
    "authority/language/"
)

WORK_HAS_EXPRESSION = URIRef(
    f"{CDM_URI_PREFIX}work_has_expression"
)

EXPRESSION_BELONGS_TO_WORK = URIRef(
    f"{CDM_URI_PREFIX}expression_belongs_to_work"
)

EXPRESSION_TITLE = URIRef(
    f"{CDM_URI_PREFIX}expression_title"
)

EXPRESSION_USES_LANGUAGE = URIRef(
    f"{CDM_URI_PREFIX}expression_uses_language"
)

LANGUAGE_CODE_MAPPING = {
    "en": "ENG",
    "fr": "FRA",
}


class MetadataExtractor:
    """Extract metadata describing a legal document."""

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

        titles = self._extract_titles(
            graph,
            document_uri,
        )

        title = self._select_preferred_title(
            titles
        )

        document_type = self._extract_document_type(
            graph,
            document_uri,
        )

        rdf_types = self._extract_rdf_types(
            graph,
            document_uri,
        )

        return DocumentMetadata(
            celex=celex,
            title=title,
            titles=titles,
            eli=eli,
            cellar_id=cellar_id,
            document_type=document_type,
            rdf_types=rdf_types,
        )

    def _extract_titles(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> dict[str, str]:
        titles: dict[str, str] = {}

        for work_uri in self._equivalent_document_uris(
            graph,
            document_uri,
        ):
            for expression_uri in self._expression_uris(
                graph,
                work_uri,
            ):
                language = self._extract_expression_language(
                    graph,
                    expression_uri,
                )

                expression_title = (
                    self._extract_expression_title(
                        graph,
                        expression_uri,
                    )
                )

                if (
                    language is None
                    or expression_title is None
                    or language in titles
                ):
                    continue

                titles[language] = expression_title

        return titles

    def _expression_uris(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> set[URIRef]:
        expression_uris: set[URIRef] = set()

        for expression_uri in graph.objects(
            document_uri,
            WORK_HAS_EXPRESSION,
        ):
            if isinstance(expression_uri, URIRef):
                expression_uris.add(expression_uri)

        for expression_uri in graph.subjects(
            EXPRESSION_BELONGS_TO_WORK,
            document_uri,
        ):
            if isinstance(expression_uri, URIRef):
                expression_uris.add(expression_uri)

        return expression_uris

    def _extract_expression_title(
        self,
        graph: Graph,
        expression_uri: URIRef,
    ) -> str | None:
        for title_value in graph.objects(
            expression_uri,
            EXPRESSION_TITLE,
        ):
            if not isinstance(title_value, Literal):
                continue

            title = str(title_value).strip()

            if title:
                return title

        return None

    def _extract_expression_language(
        self,
        graph: Graph,
        expression_uri: URIRef,
    ) -> str | None:
        for language_uri in graph.objects(
            expression_uri,
            EXPRESSION_USES_LANGUAGE,
        ):
            language = self._language_from_uri(
                language_uri
            )

            if language is not None:
                return language

        language_from_expression_uri = (
            self._language_from_expression_uri(
                expression_uri
            )
        )

        if language_from_expression_uri is not None:
            return language_from_expression_uri

        for title_value in graph.objects(
            expression_uri,
            EXPRESSION_TITLE,
        ):
            if not isinstance(title_value, Literal):
                continue

            language = self._language_from_literal(
                title_value
            )

            if language is not None:
                return language

        return None

    def _select_preferred_title(
        self,
        titles: dict[str, str],
    ) -> str | None:
        english_title = titles.get("ENG")

        if english_title is not None:
            return english_title

        french_title = titles.get("FRA")

        if french_title is not None:
            return french_title

        if not titles:
            return None

        first_language = sorted(titles)[0]

        return titles[first_language]

    def _equivalent_document_uris(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> set[URIRef]:
        document_uris = {document_uri}

        for same_as in graph.objects(
            document_uri,
            OWL.sameAs,
        ):
            if isinstance(same_as, URIRef):
                document_uris.add(same_as)

        for alias_subject in graph.subjects(
            OWL.sameAs,
            document_uri,
        ):
            if isinstance(alias_subject, URIRef):
                document_uris.add(alias_subject)

            for same_as in graph.objects(
                alias_subject,
                OWL.sameAs,
            ):
                if isinstance(same_as, URIRef):
                    document_uris.add(same_as)

        return document_uris

    def _language_from_uri(
        self,
        uri: object,
    ) -> str | None:
        if not isinstance(uri, URIRef):
            return None

        uri_value = str(uri)

        if not uri_value.startswith(
            LANGUAGE_URI_PREFIX
        ):
            return None

        language = uri_value.removeprefix(
            LANGUAGE_URI_PREFIX
        ).strip()

        if not language:
            return None

        return language.upper()

    def _language_from_expression_uri(
        self,
        expression_uri: URIRef,
    ) -> str | None:
        uri_value = str(expression_uri)

        if "." not in uri_value:
            return None

        language = uri_value.rsplit(
            ".",
            maxsplit=1,
        )[-1].strip()

        if len(language) != 3:
            return None

        if not language.isalpha():
            return None

        return language.upper()

    def _language_from_literal(
        self,
        literal: Literal,
    ) -> str | None:
        if literal.language is None:
            return None

        language = literal.language.lower()

        mapped_language = LANGUAGE_CODE_MAPPING.get(
            language
        )

        if mapped_language is not None:
            return mapped_language

        if len(language) == 3 and language.isalpha():
            return language.upper()

        return None

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

    def _extract_document_type(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> str | None:
        value = graph.value(
            document_uri,
            RESOURCE_LEGAL_TYPE,
        )

        if value is None:
            return None

        document_type = str(value).strip()

        return document_type or None

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


        
    def _extract_rdf_types(
        self,
        graph: Graph,
        document_uri: URIRef,
    ) -> tuple[str, ...]:
        rdf_types = []

        for value in graph.objects(
            document_uri,
            RDF.type,
        ):
            value_str = str(value)

            if "#" in value_str:
                rdf_type = value_str.rsplit("#", 1)[-1]
            else:
                rdf_type = value_str.rstrip("/").rsplit("/", 1)[-1]

            rdf_type = rdf_type.strip()

            if rdf_type:
                rdf_types.append(rdf_type)

        return tuple(sorted(set(rdf_types)))
