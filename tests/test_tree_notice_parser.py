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

    assert (
        notice.work_uri
        == "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_parse_tree_notice_sameas_contains_celex() -> None:
    xml = FIXTURE_PATH.read_bytes()

    notice = TreeNoticeParser().parse_bytes(xml)

    assert (
        "http://publications.europa.eu/resource/celex/32022R2554"
        in notice.same_as
    )