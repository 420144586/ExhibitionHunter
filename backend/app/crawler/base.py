"""Base spider abstraction.

Subclasses implement either:
  - The simple path: set `start_urls` + implement `parse()` (one page per URL).
  - The paginated path: override `crawl()` to manage page iteration and
    early termination themselves, yielding ExhibitionCreate items directly.

The base class handles:
  - HTTP fetching (httpx for static, Playwright for JS-rendered)
  - Logging & error isolation
  - HTTP client lifecycle
"""
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

import httpx
from loguru import logger

from app.core.config import settings
from app.schemas.exhibition import ExhibitionCreate


class BaseSpider(ABC):
    name: str = "base"
    start_urls: list[str] = []
    # "httpx" | "playwright" | "auto" (auto = httpx first, fallback to playwright)
    engine: str = "auto"

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def _get_httpx(self, url: str) -> str:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "User-Agent": settings.crawler_user_agent,
                    "Accept": (
                        "text/html,application/xhtml+xml,application/xml;"
                        "q=0.9,image/avif,image/webp,*/*;q=0.8"
                    ),
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                },
                timeout=30.0,
                follow_redirects=True,
            )
        resp = await self._client.get(url)
        resp.raise_for_status()
        return resp.text

    async def _get_playwright(self, url: str, wait_selector: str | None = None) -> str:
        # Lazy import keeps httpx-only environments working
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                if wait_selector:
                    await page.wait_for_selector(wait_selector, timeout=15000)
                return await page.content()
            finally:
                await browser.close()

    async def fetch(self, url: str, wait_selector: str | None = None) -> str:
        """Fetch page HTML using the configured engine."""
        engine = self.engine if self.engine != "auto" else settings.crawler_default_engine
        if engine == "auto":
            try:
                return await self._get_httpx(url)
            except Exception as e:  # noqa: BLE001
                logger.debug(f"[{self.name}] httpx failed ({e}), falling back to playwright")
                return await self._get_playwright(url, wait_selector)
        if engine == "playwright":
            return await self._get_playwright(url, wait_selector)
        return await self._get_httpx(url)

    @abstractmethod
    async def parse(self, html: str, url: str) -> AsyncIterator[ExhibitionCreate]:
        """Parse a single page's HTML and yield ExhibitionCreate items.

        Required even for paginated spiders (used by the default `run()` path);
        paginated spiders override `crawl()` instead and may leave this as a stub.
        """
        ...
        # pragma: no cover - abstract
        if False:
            yield  # type: ignore[unreachable]

    async def crawl(self) -> AsyncIterator[ExhibitionCreate]:
        """Override to manage pagination / early termination manually.

        Default implementation delegates to `start_urls` + `parse()`.
        """
        for url in self.start_urls:
            try:
                logger.info(f"[{self.name}] fetching {url}")
                html = await self.fetch(url)
                async for item in self.parse(html, url):
                    yield item
            except Exception as e:  # noqa: BLE001
                logger.exception(f"[{self.name}] error on {url}: {e}")
                continue

    async def run(self) -> AsyncIterator[ExhibitionCreate]:
        """Entry point used by the pipeline. Delegates to `crawl()`."""
        try:
            async for item in self.crawl():
                yield item
        finally:
            if self._client is not None:
                await self._client.aclose()
                self._client = None

    async def __aenter__(self) -> "BaseSpider":
        return self

    async def __aexit__(self, exc: Any) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None
