from __future__ import annotations

import httpx

from .exceptions import InvalidCelexError, NoticeDownloadError
from .types import NoticeType


class CellarClient:
    """Client for downloading EUR-Lex / Cellar metadata notices."""

    BASE_URL = "https://publications.europa.eu"
    RESOURCE_ROOT = "/resource"
    CELEX_PATH = "/celex/{celex}"
    DEFAULT_DECODING_LANGUAGE = "eng"

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
        *,
        language: str = DEFAULT_DECODING_LANGUAGE,
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

        params = None

        if notice is NoticeType.TREE:
            params = {
                "language": language,
            }

        try:
            response = self._client.get(
                url,
                params=params,
                headers={
                    "Accept": notice.accept_header,
                },
                follow_redirects=True,
            )
            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise NoticeDownloadError(
                f"Could not download Cellar notice for CELEX {celex}."
            ) from exc

        return response.content