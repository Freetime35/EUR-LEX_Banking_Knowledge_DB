from __future__ import annotations

import httpx

from .exceptions import InvalidCelexError
from .types import NoticeType


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

    def download_notice(
        self,
        celex: str,
        notice: NoticeType = NoticeType.OBJECT,
    ) -> bytes:
        if not celex.strip():
            raise InvalidCelexError(
                "CELEX identifier cannot be empty."
            )

        raise NotImplementedError