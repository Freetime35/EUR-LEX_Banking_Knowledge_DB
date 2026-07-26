from ekb.connectors.http import (
    DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT,
    HttpClient,
)


def test_http_client_defaults():
    client = HttpClient()

    assert client.timeout == DEFAULT_TIMEOUT
    assert client.user_agent == DEFAULT_USER_AGENT

    client.close()


def test_http_client_headers():
    client = HttpClient()

    assert (
        client.client.headers["User-Agent"]
        == DEFAULT_USER_AGENT
    )

    client.close()