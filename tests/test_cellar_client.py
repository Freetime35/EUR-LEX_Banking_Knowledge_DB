import pytest

from ekb.clients.exceptions import InvalidCelexError


from ekb.clients import CellarClient, NoticeType
from ekb.clients.exceptions import InvalidCelexError

def test_default_base_url():
    assert (
        CellarClient.BASE_URL
        == "https://publications.europa.eu/resource"
    )


def test_download_notice_rejects_empty_celex():
    client = CellarClient()

    with pytest.raises(InvalidCelexError):
        client.download_notice(
            celex="",
            notice=NoticeType.OBJECT,
        )