from pathlib import Path
from xml.etree import ElementTree


FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "cellar"
    / "32022R2554_tree.xml"
)


def test_tree_notice_fixture_is_valid_xml() -> None:
    root = ElementTree.parse(FIXTURE_PATH).getroot()

    assert root.tag == "NOTICE"
    assert root.attrib["type"] == "tree"
    assert root.attrib["decoding"] == "eng"


def test_tree_notice_fixture_contains_work() -> None:
    root = ElementTree.parse(FIXTURE_PATH).getroot()

    work = root.find("WORK")

    assert work is not None


def test_tree_notice_fixture_contains_cellar_work_uri() -> None:
    root = ElementTree.parse(FIXTURE_PATH).getroot()

    work_uri = root.findtext("./WORK/URI/VALUE")

    assert work_uri == (
        "http://publications.europa.eu/resource/cellar/"
        "0caf473a-85bd-11ed-9887-01aa75ed71a1"
    )


def test_tree_notice_fixture_contains_celex_sameas_uri() -> None:
    root = ElementTree.parse(FIXTURE_PATH).getroot()

    sameas_uris = [
        value.text
        for value in root.findall("./WORK/SAMEAS/URI/VALUE")
        if value.text is not None
    ]

    assert (
        "http://publications.europa.eu/resource/celex/32022R2554"
        in sameas_uris
    )