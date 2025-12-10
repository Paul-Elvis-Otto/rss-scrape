from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import warnings

import feedparser
import httpx
from dateutil import parser as dateparser, tz
from dateutil.parser import ParserError, UnknownTimezoneWarning


TZINFOS = {
    "CET": tz.gettz("Europe/Berlin"),
    "CEST": tz.gettz("Europe/Berlin"),
    "GMT": tz.tzutc(),
    "UTC": tz.tzutc(),
}


@dataclass(slots=True)
class ArticleIn:
    title: str
    url: str
    published_at: datetime | None
    category: str | None
    platform: str


class BaseScraper(ABC):
    platform: str
    feeds: list[str]

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=20)

    @abstractmethod
    def infer_category(self, entry: dict) -> str | None:
        """
        Site-specific category logic.
        Default implementations in subclasses can be simple.
        """
        raise NotImplementedError

    def parse_datetime(self, entry: dict) -> datetime | None:
        # Most feeds have one of these
        for key in ("published", "updated", "pubDate"):
            val = entry.get(key)
            if val:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UnknownTimezoneWarning)
                    try:
                        return dateparser.parse(val, tzinfos=TZINFOS)
                    except (ParserError, ValueError, TypeError):
                        continue
        return None

    def normalize_entry(self, entry: dict) -> ArticleIn | None:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()

        if not title or not link:
            return None

        cat = self.infer_category(entry)

        return ArticleIn(
            title=title,
            url=link,
            published_at=self.parse_datetime(entry),
            category=cat,
            platform=self.platform,
        )

    def fetch_feed(self, feed_url: str) -> feedparser.FeedParserDict:
        r = self.client.get(feed_url, headers={"User-Agent": "rss-scraper/1.0"})
        r.raise_for_status()
        return feedparser.parse(r.text)

    def scrape(self) -> list[ArticleIn]:
        items: list[ArticleIn] = []

        for feed_url in self.feeds:
            parsed = self.fetch_feed(feed_url)
            for entry in parsed.entries:
                art = self.normalize_entry(entry)
                if art:
                    items.append(art)

        return items

    def close(self) -> None:
        self.client.close()
