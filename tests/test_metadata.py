from pathlib import Path

from rdflib import Graph, URIRef

from ekb.extractors.metadata import MetadataExtractor


def test_extract_metadata_from_real_notice():
    project_root = Path(__file__).resolve().parents[1]
    notice_path = project_root / "notice.xml"

    graph = Graph()
    graph.parse(notice_path)

    document_uri = URIRef(
        "http://publications.europa.eu/resource/celex/32022R2554"
    )

    metadata = MetadataExtractor().extract(
        graph,
        document_uri,
    )

    assert metadata is not None

    print("\nMetadata:", metadata)
    print("Preferred title:", metadata.title)
    print("All titles:", metadata.titles)

    assert metadata.celex == "32022R2554"
    assert metadata.title is None
    assert metadata.titles == {}