import httpx
import pytest

from ekb.clients import CellarClient, NoticeType


@pytest.mark.integration
def test_download_real_tree_notice() -> None:
    celex = "32022R2554"

    with httpx.Client(timeout=30.0) as http_client:
        client = CellarClient(client=http_client)

        xml_content = client.download_notice(
            celex=celex,
            notice=NoticeType.TREE,
        )

    assert xml_content
    assert b"<NOTICE" in xml_content
    assert b'type="tree"' in xml_content
    assert b'decoding="eng"' in xml_content
    assert b"<WORK>" in xml_content