"""Reusable HTTP client."""

from __future__ import annotations

import httpx


DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "ekb/0.1.0"


class HttpClient:
    """Small wrapper around httpx.Client."""

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.timeout = timeout
        self.user_agent = user_agent

        self._client = httpx.Client(
            timeout=timeout,
            headers={
                "User-Agent": user_agent,
            },
            follow_redirects=True,
        )

    @property
    def client(self) -> httpx.Client:
        """Return the underlying httpx client."""
        return self._client

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()