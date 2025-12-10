from __future__ import annotations

from ..base import BaseScraper


class DWScraper(BaseScraper):
    platform = "Deutsche Welle"
    feeds = [
        "https://rss.dw.com/rdf/rss-en-all",
        "https://rss.dw.com/rdf/rss-en-world",
    ]

    def infer_category(self, entry: dict) -> str | None:
        # DW sometimes uses tags/categories
        tags = entry.get("tags") or []
        if tags:
            term = tags[0].get("term")
            return term.strip() if term else None
        # Some feeds have 'category'
        cat = entry.get("category")
        return cat.strip() if isinstance(cat, str) and cat.strip() else None
