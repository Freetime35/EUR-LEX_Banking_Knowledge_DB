from rdflib import RDF, Graph, URIRef

from ekb.extractors.document import CDM, DocumentExtractor


def test_extract_returns_legal_documents() -> None:
    graph = Graph()

    first_uri = URIRef(
        "http://publications.europa.eu/resource/oj/JOL_2022_333_R_0001"
    )
    second_uri = URIRef(
        "http://publications.europa.eu/resource/oj/JOL_2022_333_R_0002"
    )

    graph.add((first_uri, RDF.type, CDM.resource_legal))
    graph.add((second_uri, RDF.type, CDM.resource_legal))

    documents = DocumentExtractor().extract(graph)

    assert [document.uri for document in documents] == [
        first_uri,
        second_uri,
    ]


def test_extract_ignores_non_legal_resources() -> None:
    graph = Graph()

    legal_uri = URIRef(
        "http://publications.europa.eu/resource/oj/JOL_2022_333_R_0001"
    )
    expression_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001.ENG"
    )

    graph.add((legal_uri, RDF.type, CDM.resource_legal))
    graph.add((expression_uri, RDF.type, CDM.expression))

    documents = DocumentExtractor().extract(graph)

    assert len(documents) == 1
    assert documents[0].uri == legal_uri


def test_extract_ignores_blank_nodes() -> None:
    graph = Graph()

    legal_uri = URIRef(
        "http://publications.europa.eu/resource/oj/JOL_2022_333_R_0001"
    )

    graph.add((legal_uri, RDF.type, CDM.resource_legal))

    documents = DocumentExtractor().extract(graph)

    assert all(isinstance(document.uri, URIRef) for document in documents)


def test_extract_returns_empty_list_when_no_documents_exist() -> None:
    graph = Graph()

    documents = DocumentExtractor().extract(graph)

    assert documents == []