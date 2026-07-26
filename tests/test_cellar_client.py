from ekb.clients import CellarClient


def test_default_base_url():
    assert (
        CellarClient.BASE_URL
        == "https://publications.europa.eu/resource"
    )