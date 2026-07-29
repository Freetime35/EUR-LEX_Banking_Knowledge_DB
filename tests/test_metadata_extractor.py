from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, RDF

from ekb.extractors.metadata import MetadataExtractor

CDM = Namespace(
    "http://publications.europa.eu/ontology/cdm#"
)



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


def test_extracts_direct_eli() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/eli/"
        "reg/2022/2554/oj"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32022R2554"
    assert metadata.eli == str(document_uri)


def test_extracts_eli_from_same_as() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://example.com/document"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )
    eli_uri = URIRef(
        "http://publications.europa.eu/resource/eli/"
        "reg/2022/2554/oj"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))
    graph.add((document_uri, OWL.sameAs, eli_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32022R2554"
    assert metadata.eli == str(eli_uri)


def test_extracts_eli_through_shared_cellar_alias() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )
    eli_uri = URIRef(
        "http://publications.europa.eu/resource/eli/"
        "reg/2022/2554/oj"
    )

    graph.add((cellar_uri, OWL.sameAs, document_uri))
    graph.add((cellar_uri, OWL.sameAs, celex_uri))
    graph.add((cellar_uri, OWL.sameAs, eli_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32022R2554"
    assert metadata.eli == str(eli_uri)


def test_returns_none_when_no_eli() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/test"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((cellar_uri, OWL.sameAs, document_uri))
    graph.add((cellar_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.celex == "32022R2554"
    assert metadata.eli is None



def test_extracts_direct_cellar_id() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.cellar_id == (
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_extracts_cellar_id_from_same_as() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))
    graph.add((document_uri, OWL.sameAs, cellar_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.cellar_id == (
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_extracts_cellar_id_through_inverse_alias() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/"
        "JOL_2022_333_R_0001"
    )
    cellar_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((cellar_uri, OWL.sameAs, document_uri))
    graph.add((cellar_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.cellar_id == (
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_returns_none_when_no_cellar_id() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/oj/test"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )
    eli_uri = URIRef(
        "http://publications.europa.eu/resource/eli/"
        "reg/2022/2554/oj"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))
    graph.add((document_uri, OWL.sameAs, eli_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.cellar_id is None


def test_extracts_rdf_types() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, RDF.type, CDM.work))
    graph.add((document_uri, RDF.type, CDM.resource_legal))
    graph.add((document_uri, RDF.type, CDM.regulation))
    graph.add(
        (
            document_uri,
            RDF.type,
            CDM["official-journal-act"],
        )
    )
    graph.add(
        (
            document_uri,
            RDF.type,
            CDM.legislation_secondary,
        )
    )

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.rdf_types == (
        "legislation_secondary",
        "official-journal-act",
        "regulation",
        "resource_legal",
        "work",
    )


def test_extracts_empty_rdf_types() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/cellar/test"
    )
    celex_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, OWL.sameAs, celex_uri))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.rdf_types == ()


def test_derives_regulation_legal_type() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, RDF.type, CDM.regulation))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.legal_type == "regulation"


def test_prefers_delegated_regulation_legal_type() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, RDF.type, CDM.regulation))
    graph.add(
        (
            document_uri,
            RDF.type,
            CDM.regulation_delegated,
        )
    )

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.legal_type == "regulation_delegated"


def test_prefers_implementing_directive_legal_type() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022L2554"
    )

    graph.add((document_uri, RDF.type, CDM.directive))
    graph.add(
        (
            document_uri,
            RDF.type,
            CDM.directive_implementing,
        )
    )

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.legal_type == "directive_implementing"


def test_returns_none_when_rdf_types_have_no_known_legal_type() -> None:
    graph = Graph()

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/"
        "32022R2554"
    )

    graph.add((document_uri, RDF.type, CDM.work))
    graph.add((document_uri, RDF.type, CDM.resource_legal))

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None
    assert metadata.legal_type is None
