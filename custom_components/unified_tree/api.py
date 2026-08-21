"""Small async client for the unified TREE local API."""

from __future__ import annotations


class UnifiedTreeApi:
    def __init__(self, session, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip("/")

    async def _get(self, path: str):
        async with self.session.get(f"{self.base_url}{path}", timeout=10) as response:
            response.raise_for_status()
            return await response.json()

    async def health(self):
        return await self._get("/api/health")

    async def summary(self):
        return await self._get("/api/summary")
