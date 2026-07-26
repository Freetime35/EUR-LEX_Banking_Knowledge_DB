from ekb.models import DocumentMetadata


def test_document_metadata_defaults():
    metadata = DocumentMetadata(celex="32022R2554")

    assert metadata.celex == "32022R2554"
    assert metadata.title is None
    assert metadata.languages == []


def test_document_metadata_values():
    metadata = DocumentMetadata(
        celex="32022R2554",
        title="Digital Operational Resilience Act",
        languages=["en", "fr"],
    )

    assert metadata.title == "Digital Operational Resilience Act"
    assert metadata.languages == ["en", "fr"]