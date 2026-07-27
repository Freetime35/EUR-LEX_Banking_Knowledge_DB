from xml.etree import ElementTree

from .models import Expression, Item, Manifestation, TreeNotice


class TreeNoticeParser:
    """Parse Cellar Tree Notice XML documents."""

    def parse_bytes(self, xml: bytes) -> TreeNotice:
        root = ElementTree.fromstring(xml)

        work_uri = root.findtext("./WORK/URI/VALUE")

        if work_uri is None:
            raise ValueError(
                "Tree Notice does not contain a WORK URI."
            )

        celex_id = root.findtext("./WORK/ID_CELEX/VALUE")

        if celex_id is None:
            raise ValueError(
                "Tree Notice does not contain a WORK CELEX identifier."
            )

        resource_legal_type = root.findtext(
            "./WORK/RESOURCE_LEGAL_TYPE/VALUE"
        )

        if resource_legal_type is None:
            raise ValueError(
                "Tree Notice does not contain a WORK resource legal type."
            )

        document_date = root.findtext(
            "./WORK/WORK_DATE_DOCUMENT/VALUE"
        )

        if document_date is None:
            raise ValueError(
                "Tree Notice does not contain a WORK document date."
            )

        document_id = root.findtext(
            "./WORK/WORK_ID_DOCUMENT/VALUE"
        )

        if document_id is None:
            raise ValueError(
                "Tree Notice does not contain a WORK document identifier."
            )

        legal_event = root.findtext(
            "./WORK/WORK_PART_OF_EVENT_LEGAL/SAMEAS/URI/IDENTIFIER"
        )

        if legal_event is None:
            raise ValueError(
                "Tree Notice does not contain a WORK legal event."
            )

        year = root.findtext(
            "./WORK/RESOURCE_LEGAL_YEAR/VALUE"
        )

        if year is None:
            raise ValueError(
                "Tree Notice does not contain a RESOURCE_LEGAL year."
            )

        treaty_basis = root.findtext(
            "./WORK/RESOURCE_LEGAL_BASED_ON_CONCEPT_TREATY/OP-CODE"
        )

        if treaty_basis is None:
            raise ValueError(
                "Tree Notice does not contain a RESOURCE_LEGAL treaty basis."
            )

        subject_matters = tuple(
            element.text
            for element in root.findall(
                "./WORK/"
                "RESOURCE_LEGAL_IS_ABOUT_SUBJECT-MATTER/"
                "RESOURCE_LEGAL_IS_ABOUT_SUBJECT-MATTER_1/"
                "OP-CODE"
            )
            if element.text is not None
        )

        creators = tuple(
            element.text
            for element in root.findall(
                "./WORK/WORK_CREATED_BY_AGENT/OP-CODE"
            )
            if element.text is not None
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
            celex_id=celex_id,
            resource_legal_type=resource_legal_type,
            document_date=document_date,
            document_id=document_id,
            legal_event=legal_event,
            year=year,
            treaty_basis=treaty_basis,
            subject_matters=subject_matters,
            creators=creators,
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

        expression_uri = element.findtext(
            "./MANIFESTATION_MANIFESTS_EXPRESSION/URI/VALUE"
        )

        if expression_uri is None:
            raise ValueError(
                "Tree Notice contains a MANIFESTATION "
                "without an Expression URI."
            )

        media_type = element.findtext(
            "./MANIFESTATION_TYPE/VALUE"
        )

        if media_type is None:
            raise ValueError(
                "Tree Notice contains a MANIFESTATION "
                "without a media type."
            )

        items = tuple(
            self._parse_item(item_element)
            for item_element in element.findall(
                "./MANIFESTATION_HAS_ITEM"
            )
        )

        return Manifestation(
            uri=uri,
            same_as=same_as,
            expression_uri=expression_uri,
            media_type=media_type,
            items=items,
        )

    def _parse_item(
        self,
        element: ElementTree.Element,
    ) -> Item:
        uri = element.findtext("./URI/VALUE")

        if uri is None:
            raise ValueError(
                "Tree Notice contains an ITEM without a URI."
            )

        identifier = element.findtext("./IDENTIFIER/VALUE")

        if identifier is None:
            raise ValueError(
                "Tree Notice contains an ITEM without an identifier."
            )

        filename = element.findtext(
            "./TECHMD/STREAM_NAME/VALUE"
        )

        if filename is None:
            raise ValueError(
                "Tree Notice contains an ITEM without a filename."
            )

        size_text = element.findtext(
            "./TECHMD/STREAM_SIZE/VALUE"
        )

        if size_text is None:
            raise ValueError(
                "Tree Notice contains an ITEM without a stream size."
            )

        try:
            size = int(size_text)
        except ValueError as error:
            raise ValueError(
                "Tree Notice contains an ITEM with an invalid stream size."
            ) from error

        order_text = element.findtext(
            "./TECHMD/STREAM_ORDER/VALUE"
        )

        if order_text is None:
            raise ValueError(
                "Tree Notice contains an ITEM without a stream order."
            )

        try:
            order = int(order_text)
        except ValueError as error:
            raise ValueError(
                "Tree Notice contains an ITEM with an invalid stream order."
            ) from error

        label = element.findtext(
            "./TECHMD/STREAM_LABEL/VALUE"
        )

        if label is None:
            raise ValueError(
                "Tree Notice contains an ITEM without a stream label."
            )

        composition_level_text = element.findtext(
            "./TECHMD/STREAM_COMPOSITION_LEVEL/VALUE"
        )

        if composition_level_text is None:
            raise ValueError(
                "Tree Notice contains an ITEM "
                "without a stream composition level."
            )

        try:
            composition_level = int(composition_level_text)
        except ValueError as error:
            raise ValueError(
                "Tree Notice contains an ITEM with an invalid "
                "stream composition level."
            ) from error

        return Item(
            uri=uri,
            identifier=identifier,
            filename=filename,
            size=size,
            order=order,
            label=label,
            composition_level=composition_level,
        )

