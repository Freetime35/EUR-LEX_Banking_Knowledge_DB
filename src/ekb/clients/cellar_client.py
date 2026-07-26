from __future__ import annotations

import httpx


class CellarClient:
    """Client for downloading EUR-Lex / Cellar metadata notices."""

    BASE_URL = "https://publications.europa.eu/resource"

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client(timeout=timeout)