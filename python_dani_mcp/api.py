"""Async client for the danielavila.me API."""

from __future__ import annotations

import os
import time
from typing import Any

import httpx2
from fastmcp.exceptions import ToolError

DEFAULT_BASE_URL = "https://www.danielavila.me/api"

# Cloudflare in front of danielavila.me rejects requests without a User-Agent (403).
DEFAULT_HEADERS = {"User-Agent": "DaniMCP/2.0", "Accept": "application/json"}


class DaniAPI:
    """Thin wrapper over the portfolio API with a per-process TTL cache for GETs.

    The data behind the API changes rarely, so caching avoids hitting the
    upstream on every tool call (and on every warm serverless invocation).
    Errors are raised as ``ToolError`` so the model receives a readable message
    instead of a stack trace.
    """

    def __init__(
        self,
        base_url: str | None = None,
        *,
        timeout: float = 10.0,
        cache_ttl: float = 300.0,
        transport: httpx2.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = (base_url or os.environ.get("DANIMCP_API_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self._transport = transport
        self._cache: dict[str, tuple[float, Any]] = {}

    def _client(self) -> httpx2.AsyncClient:
        # A client per call: stateless HTTP / serverless runtimes may not reuse
        # the same event loop between requests, so a long-lived client is unsafe.
        return httpx2.AsyncClient(
            base_url=self.base_url,
            headers=DEFAULT_HEADERS,
            timeout=self.timeout,
            follow_redirects=True,
            transport=self._transport,
        )

    async def _request(self, method: str, endpoint: str, json: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            async with self._client() as client:
                response = await client.request(method, f"/{endpoint}", json=json)
                response.raise_for_status()
                return response.json()
        except httpx2.TimeoutException as e:
            raise ToolError(f"Request to {url} timed out after {self.timeout:.0f}s") from e
        except httpx2.HTTPStatusError as e:
            raise ToolError(f"{method} {url} failed with HTTP {e.response.status_code}") from e
        except httpx2.HTTPError as e:
            raise ToolError(f"Could not reach {url}: {e}") from e
        except ValueError as e:
            raise ToolError(f"{method} {url} returned a non-JSON response") from e

    async def get(self, endpoint: str) -> Any:
        cached = self._cache.get(endpoint)
        if cached and time.monotonic() - cached[0] < self.cache_ttl:
            return cached[1]
        data = await self._request("GET", endpoint)
        self._cache[endpoint] = (time.monotonic(), data)
        return data

    async def post(self, endpoint: str, payload: dict[str, Any]) -> Any:
        return await self._request("POST", endpoint, json=payload)
