"""Reusable HTTP client."""

from __future__ import annotations

from collections.abc import Mapping

import httpx

from .exceptions import RemoteServiceError, ResourceNotFoundError


DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "ekb/0.1.0"


class HttpClient:
    """Small wrapper around httpx.Client."""

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.timeout = timeout
        self.user_agent = user_agent

        self._client = httpx.Client(
            timeout=timeout,
            headers={"User-Agent": user_agent},
            follow_redirects=True,
            transport=transport,
        )

    @property
    def client(self) -> httpx.Client:
        """Return the underlying httpx client."""
        return self._client

    def get(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        """Perform a GET request and translate common HTTP errors."""
        try:
            response = self._client.get(url, headers=headers)
        except httpx.HTTPError as exc:
            raise RemoteServiceError(
                f"Unable to contact remote service: {url}"
            ) from exc

        if response.status_code == 404:
            raise ResourceNotFoundError(
                f"Remote resource was not found: {url}"
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RemoteServiceError(
                f"Remote service returned HTTP {response.status_code}: {url}"
            ) from exc

        return response

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> HttpClient:
        """Enter the context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Close the client when leaving the context manager."""
        self.close()