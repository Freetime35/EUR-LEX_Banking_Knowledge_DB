"""Cellar connector."""

from __future__ import annotations

import re

from .base import BaseConnector
from .http import HttpClient

CELLAR_RESOURCE_BASE_URL = (
    "https://publications.europa.eu/resource/celex"
)
RDF_XML_MEDIA_TYPE = "application/rdf+xml"

CELEX_PATTERN = re.compile(r"^[0-9A-Z()_-]+$")


class CellarClient(BaseConnector):
    """Client for the Publications Office Cellar service."""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.http_client = http_client or HttpClient()
        self._owns_http_client = http_client is None

    def get_metadata_notice(self, celex: str) -> str:
        """Retrieve the RDF/XML metadata notice for a CELEX identifier."""
        normalized_celex = self._normalize_celex(celex)
        url = f"{CELLAR_RESOURCE_BASE_URL}/{normalized_celex}"

        response = self.http_client.get(
            url,
            headers={"Accept": RDF_XML_MEDIA_TYPE},
        )

        return response.text

    @staticmethod
    def _normalize_celex(celex: str) -> str:
        """Normalize and validate a CELEX identifier."""
        normalized = celex.strip().upper()

        if not normalized:
            raise ValueError("CELEX identifier cannot be empty.")

        if not CELEX_PATTERN.fullmatch(normalized):
            raise ValueError(
                f"Invalid CELEX identifier: {celex!r}"
            )

        return normalized

    def close(self) -> None:
        """Close the internally created HTTP client."""
        if self._owns_http_client:
            self.http_client.close()

    def __enter__(self) -> CellarClient:
        """Enter the context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Close the connector when leaving the context manager."""
        self.close()