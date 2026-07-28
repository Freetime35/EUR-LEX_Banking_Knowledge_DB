from pathlib import Path

from rdflib import Graph


def test_fixture_tree_notice_is_valid_rdf() -> None:
    rdf_file = Path("tests/fixtures/cellar/32022R2554_tree.rdf")

    assert rdf_file.exists()

    graph = Graph()
    graph.parse(rdf_file)

    assert len(graph) > 0