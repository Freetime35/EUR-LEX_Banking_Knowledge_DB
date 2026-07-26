import httpx
import pytest

from ekb.clients import CellarClient, NoticeType
from ekb.clients.exceptions import (
    InvalidCelexError,
    NoticeDownloadError,
)


def test_default_url_constants():
    assert CellarClient.BASE_URL == "https://publications.europa.eu"
    assert CellarClient.RESOURCE_ROOT == "/resource"
    assert CellarClient.CELEX_PATH == "/celex/{celex}"


def test_download_notice_rejects_empty_celex():
    client = CellarClient()

    with pytest.raises(InvalidCelexError):
        client.download_notice(
            celex="",
            notice=NoticeType.OBJECT,
        )


def test_downloads_tree_notice():
    rdf_content = b"<rdf:RDF />"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == "https://publications.europa.eu/resource/celex/32022R2554"
        )
        assert (
            request.headers["Accept"]
            == "application/rdf+xml;notice=tree"
        )

        return httpx.Response(
            status_code=200,
            content=rdf_content,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.TREE,
        )

    assert result == rdf_content


def test_download_notice_wraps_http_status_errors():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=404,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        with pytest.raises(NoticeDownloadError) as exc_info:
            client.download_notice(
                celex="32022R2554",
                notice=NoticeType.OBJECT,
            )

    assert "32022R2554" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, httpx.HTTPStatusError)


def test_download_notice_wraps_network_errors():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(
            "Connection failed.",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        with pytest.raises(NoticeDownloadError) as exc_info:
            client.download_notice(
                celex="32022R2554",
                notice=NoticeType.TREE,
            )

    assert "32022R2554" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, httpx.ConnectError)