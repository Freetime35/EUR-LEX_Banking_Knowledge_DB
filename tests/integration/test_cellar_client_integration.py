import httpx
import pytest
from rdflib import Graph

from ekb.clients import CellarClient, NoticeType


@pytest.mark.integration
def test_download_real_tree_notice() -> None:
    celex = "32022R2554"

    with httpx.Client(timeout=30.0) as http_client:
        client = CellarClient(client=http_client)

        rdf_content = client.download_notice(
            celex=celex,
            notice=NoticeType.TREE,
        )

    assert rdf_content
    assert b"rdf:RDF" in rdf_content

    graph = Graph()
    graph.parse(
        data=rdf_content,
        format="xml",
    )

    assert len(graph) > 0