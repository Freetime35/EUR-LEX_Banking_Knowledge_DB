from xml.etree import ElementTree

from .models import TreeNotice


class TreeNoticeParser:
    """Parse Cellar Tree Notice XML documents."""

    def parse_bytes(self, xml: bytes) -> TreeNotice:
        root = ElementTree.fromstring(xml)

        work_uri = root.findtext("./WORK/URI/VALUE")

        if work_uri is None:
            raise ValueError(
                "Tree Notice does not contain a WORK URI."
            )

        same_as = tuple(
            value.text
            for value in root.findall("./WORK/SAMEAS/URI/VALUE")
            if value.text is not None
        )

        return TreeNotice(
            work_uri=work_uri,
            same_as=same_as,
        )