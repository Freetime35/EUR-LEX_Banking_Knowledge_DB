from __future__ import annotations

import httpx

from .exceptions import InvalidCelexError
from .types import NoticeType


class CellarClient:
    """Client for downloading EUR-Lex / Cellar metadata notices."""

    BASE_URL = "https://publications.europa.eu"
    RESOURCE_ROOT = "/resource"
    CELEX_PATH = "/celex/{celex}"

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
        """Download a metadata notice for a CELEX identifier."""

        celex = celex.strip()

        if not celex:
            raise InvalidCelexError(
                "CELEX identifier cannot be empty."
            )

        url = (
            f"{self.BASE_URL}"
            f"{self.RESOURCE_ROOT}"
            f"{self.CELEX_PATH.format(celex=celex)}"
        )

        response = self._client.get(
            url,
            headers={
                "Accept": notice.accept_header,
            },
        )

        response.raise_for_status()

        return response.content