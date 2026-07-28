import httpx
import pytest

from ekb.connectors.cellar import (
    CELLAR_RESOURCE_BASE_URL,
    RDF_XML_MEDIA_TYPE,
    CellarClient,
)
from ekb.connectors.exceptions import ResourceNotFoundError
from ekb.connectors.http import HttpClient

SAMPLE_RDF = """\
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
</rdf:RDF>
"""


def test_get_metadata_notice() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == (
            f"{CELLAR_RESOURCE_BASE_URL}/32022R2554"
        )
        assert request.headers["Accept"] == RDF_XML_MEDIA_TYPE

        return httpx.Response(
            status_code=200,
            text=SAMPLE_RDF,
            headers={"Content-Type": RDF_XML_MEDIA_TYPE},
        )

    transport = httpx.MockTransport(handler)
    http_client = HttpClient(transport=transport)
    cellar_client = CellarClient(http_client=http_client)

    notice = cellar_client.get_metadata_notice("32022r2554")

    assert notice == SAMPLE_RDF

    http_client.close()


def test_get_metadata_notice_rejects_empty_celex() -> None:
    cellar_client = CellarClient(
        http_client=HttpClient(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200)
            )
        )
    )

    with pytest.raises(
        ValueError,
        match="CELEX identifier cannot be empty",
    ):
        cellar_client.get_metadata_notice("   ")

    cellar_client.http_client.close()


def test_get_metadata_notice_translates_not_found() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            status_code=404,
            request=request,
        )
    )
    http_client = HttpClient(transport=transport)
    cellar_client = CellarClient(http_client=http_client)

    with pytest.raises(ResourceNotFoundError):
        cellar_client.get_metadata_notice("32022R2554")

    http_client.close()