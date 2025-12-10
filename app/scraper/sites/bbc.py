from __future__ import annotations

from ..base import BaseScraper


class BBCScraper(BaseScraper):
    platform = "BBC"
    feeds = [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
    ]

    def infer_category(self, entry: dict) -> str | None:
        # BBC often provides tags; fall back to None
        tags = entry.get("tags") or []
        if tags:
            term = tags[0].get("term")
            return term.strip() if term else None
        return None
