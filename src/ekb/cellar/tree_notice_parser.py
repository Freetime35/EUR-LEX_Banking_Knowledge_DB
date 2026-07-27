from xml.etree import ElementTree

from .models import Expression, Manifestation, TreeNotice


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

        expressions = tuple(
            self._parse_expression(element)
            for element in root.findall("./EXPRESSION")
        )

        manifestations = tuple(
            self._parse_manifestation(element)
            for element in root.findall("./MANIFESTATION")
        )

        return TreeNotice(
            work_uri=work_uri,
            same_as=same_as,
            expressions=expressions,
            manifestations=manifestations,
        )

    def _parse_expression(
        self,
        element: ElementTree.Element,
    ) -> Expression:
        uri = element.findtext("./URI/VALUE")

        if uri is None:
            raise ValueError(
                "Tree Notice contains an EXPRESSION without a URI."
            )

        language = element.findtext(
            "./EXPRESSION_USES_LANGUAGE/OP-CODE"
        )

        if language is not None:
            language = language.lower()

        return Expression(
            uri=uri,
            language=language,
        )

    def _parse_manifestation(
        self,
        element: ElementTree.Element,
    ) -> Manifestation:
        uri = element.findtext("./URI/VALUE")

        if uri is None:
            raise ValueError(
                "Tree Notice contains a MANIFESTATION without a URI."
            )

        same_as = tuple(
            value.text
            for value in element.findall("./SAMEAS/URI/VALUE")
            if value.text is not None
        )

        return Manifestation(
            uri=uri,
            same_as=same_as,
        )