import pytest
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS

from ekb.parsers.rdf import RdfParser


VALID_RDF_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dcterms="http://purl.org/dc/terms/">
    <rdf:Description rdf:about="http://example.org/document/1">
        <dcterms:title>Example document</dcterms:title>
    </rdf:Description>
</rdf:RDF>
"""


def test_parse_returns_complete_graph() -> None:
    parser = RdfParser()

    graph = parser.parse(VALID_RDF_XML)

    subject = URIRef("http://example.org/document/1")

    assert isinstance(graph, Graph)
    assert len(graph) == 1
    assert (
        subject,
        DCTERMS.title,
        Literal("Example document"),
    ) in graph


def test_parse_rejects_empty_content() -> None:
    parser = RdfParser()

    with pytest.raises(
        ValueError,
        match="RDF/XML content must not be empty",
    ):
        parser.parse("")


def test_parse_rejects_invalid_rdf_xml() -> None:
    parser = RdfParser()

    with pytest.raises(Exception):
        parser.parse("<not-valid-rdf>")