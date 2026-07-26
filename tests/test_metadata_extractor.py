from rdflib import Graph, URIRef
from rdflib.namespace import OWL

from ekb.extractors.metadata import MetadataExtractor


def test_extracts_celex_from_same_as_relation() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "db95106e-53ca-11ea-aece-01aa75ed71a1"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "52020DC0067"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "52020DC0067"


def test_decodes_url_encoded_celex() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32021R0168R%2801%29"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32021R0168R(01)"


def test_ignores_non_celex_same_as_relations() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    comnat_uri = URIRef(
        "http://publications.europa.eu/resource/comnat/"
        "COM_2020_0067"
    )

    graph.add((document_uri, OWL.sameAs, comnat_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is None


def test_returns_none_when_document_has_no_same_as() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is None