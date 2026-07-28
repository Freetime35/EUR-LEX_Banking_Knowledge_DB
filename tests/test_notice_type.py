from ekb.clients import NoticeType


def test_tree_accept_header() -> None:
    assert (
        NoticeType.TREE.accept_header
        == "application/xml;notice=tree"
    )


def test_object_accept_header() -> None:
    assert (
        NoticeType.OBJECT.accept_header
        == "application/rdf+xml"
    )