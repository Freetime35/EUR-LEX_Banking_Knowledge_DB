from pathlib import Path

from ekb.cellar import TreeNoticeParser


FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "cellar"
    / "32022R2554_tree.xml"
)


def test_parse_tree_notice_work_uri() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert notice.work_uri == (
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_parse_tree_notice_contains_celex_same_as() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert (
        "http://publications.europa.eu/resource/celex/32022R2554"
        in notice.same_as
    )


def test_parse_tree_notice_contains_expressions() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert len(notice.expressions) > 0


def test_parse_tree_notice_contains_english_expression() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert any(
        expression.language == "eng"
        for expression in notice.expressions
    )


def test_parse_tree_notice_contains_manifestations() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert len(notice.manifestations) > 0


def test_parse_tree_notice_contains_known_manifestation() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert any(
        manifestation.uri
        == (
            "http://publications.europa.eu/resource/cellar/"
            "0caf473a-85bd-11ed-9887-01aa75ed71a1.0004.01"
        )
        for manifestation in notice.manifestations
    )
def test_manifestation_contains_expression_uri() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    manifestation = notice.manifestations[0]

    assert manifestation.expression_uri.startswith(
        "http://publications.europa.eu/resource/cellar/"
    )


def test_manifestation_links_to_existing_expression() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    expression_uris = {
        expression.uri
        for expression in notice.expressions
    }

    assert all(
        manifestation.expression_uri in expression_uris
        for manifestation in notice.manifestations
    )

def test_manifestation_contains_media_type() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    manifestation = notice.manifestations[0]

    assert manifestation.media_type is not None


def test_manifestation_contains_xhtml_or_pdf_variant() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    media_types = {
        manifestation.media_type
        for manifestation in notice.manifestations
    }

    assert any(
        media_type in {"pdfa2a", "xhtml", "fmx4"}
        for media_type in media_types
    )

def test_manifestation_contains_items() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    manifestation = notice.manifestations[0]

    assert len(manifestation.items) > 0


def test_item_contains_uri_and_identifier() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.uri.endswith("/DOC_1")
    assert item.identifier == "DOC_1"


def test_item_contains_filename() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.filename == "L_2022333DE.01000101.doc.html"


def test_manifestation_item_filename_is_not_empty() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.filename

def test_item_contains_stream_size() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.size > 0


def test_item_stream_size_is_integer() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert isinstance(item.size, int)

def test_item_contains_stream_order() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.order >= 0


def test_item_stream_order_is_integer() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert isinstance(item.order, int)

def test_item_contains_stream_label() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert item.label != ""


def test_item_stream_label_is_string() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    item = notice.manifestations[0].items[0]

    assert isinstance(item.label, str)