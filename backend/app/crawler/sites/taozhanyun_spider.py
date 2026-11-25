"""淘展云 (taozhanyun.com) spider.

Server-rendered HTML table, no JS rendering needed. Lists ongoing + upcoming
exhibitions sorted by start date ascending. We crawl current year and next
year (to cover the 3-month window across year boundaries), paginate until
empty or until we pass the future-window cutoff.
"""
import hashlib
from collections.abc import AsyncIterator
from datetime import date, datetime

from loguru import logger
from selectolax.parser import HTMLParser

from app.core.config import settings
from app.crawler.base import BaseSpider
from app.schemas.exhibition import ExhibitionCreate

BASE_URL = "http://www.taozhanyun.com/meetplan.aspx"
PAGE_SIZE = 30  # rows per page on taozhanyun
MAX_PAGES = 50  # safety cap per year


class TaozhanyunSpider(BaseSpider):
    name = "taozhanyun"
    engine = "httpx"

    def __init__(self) -> None:
        super().__init__()
        self._stop = False

    @staticmethod
    def _cutoff() -> date:
        today = date.today()
        return date.fromordinal(today.toordinal() + settings.crawler_future_months * 30)

    def _build_url(self, year: int, page: int) -> str:
        return (
            f"{BASE_URL}?city=&keyword=&meetid=&month=&year={year}&page={page}"
        )

    async def parse(self, html: str, url: str) -> AsyncIterator[ExhibitionCreate]:
        """Parse one list page. Sets self._stop when a row passes the cutoff."""
        tree = HTMLParser(html)
        rows = tree.css("table tr")
        today = date.today()
        cutoff = self._cutoff()
        for row in rows[1:]:  # skip header
            cells = row.css("td")
            if len(cells) < 6:
                continue
            start_raw = cells[1].text(strip=True)
            end_raw = cells[2].text(strip=True)
            title = cells[3].text(strip=True)
            city = cells[4].text(strip=True)
            venue = cells[5].text(strip=True)
            if not title or not start_raw:
                continue
            try:
                start_date = datetime.strptime(start_raw, "%Y-%m-%d")
                end_date = datetime.strptime(end_raw, "%Y-%m-%d")
            except ValueError:
                continue
            if end_date.date() < today:
                continue  # already ended
            if start_date.date() > cutoff:
                self._stop = True
                return  # beyond window - stop crawling further pages
            sid = hashlib.md5(f"{title}|{start_raw}".encode()).hexdigest()[:16]
            yield ExhibitionCreate(
                source_site=self.name,
                source_id=sid,
                source_url=url,
                title=title,
                start_date=start_date,
                end_date=end_date,
                city=city or None,
                venue=venue or None,
            )

    async def crawl(self) -> AsyncIterator[ExhibitionCreate]:
        today = date.today()
        years = [today.year, today.year + 1]
        for year in years:
            self._stop = False
            for page in range(1, MAX_PAGES + 1):
                url = self._build_url(year, page)
                try:
                    logger.info(f"[{self.name}] fetching {url}")
                    html = await self.fetch(url)
                except Exception as e:  # noqa: BLE001
                    logger.exception(f"[{self.name}] error on {url}: {e}")
                    break  # stop this year, try next
                yielded_any = False
                async for item in self.parse(html, url):
                    yielded_any = True
                    yield item
                if self._stop:
                    logger.info(f"[{self.name}] cutoff reached at {url}")
                    break  # next year
                if not yielded_any:
                    logger.info(f"[{self.name}] no rows at {url}, stopping year {year}")
                    break  # no more pages this year
