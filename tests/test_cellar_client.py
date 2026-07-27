import httpx
import pytest

from ekb.clients import CellarClient, NoticeType
from ekb.clients.exceptions import (
    InvalidCelexError,
    NoticeDownloadError,
)


def test_default_url_constants() -> None:
    assert CellarClient.BASE_URL == "https://publications.europa.eu"
    assert CellarClient.RESOURCE_ROOT == "/resource"
    assert CellarClient.CELEX_PATH == "/celex/{celex}"


def test_download_notice_rejects_empty_celex() -> None:
    client = CellarClient()

    with pytest.raises(InvalidCelexError):
        client.download_notice(
            celex="",
            notice=NoticeType.OBJECT,
        )


def test_download_notice_rejects_whitespace_only_celex() -> None:
    client = CellarClient()

    with pytest.raises(InvalidCelexError):
        client.download_notice(
            celex="   ",
            notice=NoticeType.OBJECT,
        )


def test_downloads_object_notice_without_language_parameter() -> None:
    rdf_content = b"<rdf:RDF />"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == "https://publications.europa.eu/resource/celex/32022R2554"
        )
        assert request.headers["Accept"] == "application/rdf+xml"

        return httpx.Response(
            status_code=200,
            content=rdf_content,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.OBJECT,
        )

    assert result == rdf_content


def test_downloads_tree_notice_with_default_language() -> None:
    xml_content = b"<tree />"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == (
                "https://publications.europa.eu"
                "/resource/celex/32022R2554"
                "?language=eng"
            )
        )
        assert (
            request.headers["Accept"]
            == "application/xml;notice=tree"
        )

        return httpx.Response(
            status_code=200,
            content=xml_content,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.TREE,
        )

    assert result == xml_content


def test_downloads_tree_notice_with_requested_language() -> None:
    xml_content = b"<tree />"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == (
                "https://publications.europa.eu"
                "/resource/celex/32022R2554"
                "?language=fra"
            )
        )
        assert (
            request.headers["Accept"]
            == "application/xml;notice=tree"
        )

        return httpx.Response(
            status_code=200,
            content=xml_content,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.TREE,
            language="fra",
        )

    assert result == xml_content


def test_object_notice_ignores_tree_decoding_language() -> None:
    rdf_content = b"<rdf:RDF />"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == "https://publications.europa.eu/resource/celex/32022R2554"
        )
        assert request.headers["Accept"] == "application/rdf+xml"

        return httpx.Response(
            status_code=200,
            content=rdf_content,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.OBJECT,
            language="fra",
        )

    assert result == rdf_content


def test_download_notice_follows_redirects() -> None:
    xml_content = b"<tree />"

    initial_url = (
        "https://publications.europa.eu"
        "/resource/celex/32022R2554"
        "?language=eng"
    )
    redirected_url = (
        "http://publications.europa.eu"
        "/resource/cellar/example/tree"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == initial_url:
            return httpx.Response(
                status_code=303,
                headers={
                    "Location": redirected_url,
                },
                request=request,
            )

        assert str(request.url) == redirected_url
        assert (
            request.headers["Accept"]
            == "application/xml;notice=tree"
        )

        return httpx.Response(
            status_code=200,
            content=xml_content,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = CellarClient(client=http_client)

        result = client.download_notice(
            celex="32022R2554",
            notice=NoticeType.TREE,
        )

    assert result == xml_content


def test_download_notice_wraps_http_status_errors() -> None:
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

    assert isinstance(
        exc_info.value.__cause__,
        httpx.HTTPStatusError,
    )


def test_download_notice_wraps_network_errors() -> None:
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

    assert isinstance(
        exc_info.value.__cause__,
        httpx.ConnectError,
    )