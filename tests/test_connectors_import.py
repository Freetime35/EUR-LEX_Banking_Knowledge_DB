from ekb.connectors.cellar import CellarClient


def test_cellar_client_import():
    client = CellarClient()
    assert isinstance(client, CellarClient)