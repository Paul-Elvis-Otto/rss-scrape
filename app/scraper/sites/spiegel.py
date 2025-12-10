from __future__ import annotations

from ..base import BaseScraper


class SpiegelPoliticsScraper(BaseScraper):
    platform = "DER SPIEGEL"
    feeds = [
        "https://www.spiegel.de/politik/index.rss",
        "https://www.spiegel.de/politik/deutschland/index.rss",
        "https://www.spiegel.de/ausland/index.rss",
    ]

    def infer_category(self, entry: dict) -> str | None:
        # All feeds are politics-focused; keep a consistent category label.
        return "Politics"
