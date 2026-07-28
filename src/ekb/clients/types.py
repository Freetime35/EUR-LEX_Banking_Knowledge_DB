from enum import StrEnum


class NoticeType(StrEnum):
    """Supported Cellar metadata notice types."""

    OBJECT = "object"
    TREE = "tree"

    @property
    def accept_header(self) -> str:
        if self is NoticeType.OBJECT:
            return "application/rdf+xml"

        if self is NoticeType.TREE:
            return "application/xml;notice=tree"

        raise AssertionError(f"Unsupported notice type: {self}")