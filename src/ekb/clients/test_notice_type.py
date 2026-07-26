from ekb.clients import NoticeType


def test_tree_accept_header():
    assert (
        NoticeType.TREE.accept_header
        == "application/rdf+xml;notice=tree"
    )


def test_object_accept_header():
    assert (
        NoticeType.OBJECT.accept_header
        == "application/rdf+xml"
    )