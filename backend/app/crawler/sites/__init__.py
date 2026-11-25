"""Per-site spider implementations.

Register every spider here. The scheduler and crawl API iterate ALL_SPIDERS.
"""
from app.crawler.sites.taozhanyun_spider import TaozhanyunSpider

ALL_SPIDERS: list[type] = [
    TaozhanyunSpider,
]

__all__ = ["ALL_SPIDERS", "TaozhanyunSpider"]
