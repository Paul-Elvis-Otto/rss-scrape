from __future__ import annotations

from ..base import BaseScraper


class BILDScraper(BaseScraper):
    platform = "BILD"
    feeds = [
        "https://www.bild.de/feed/alles.xml",
    ]

    def infer_category(self, entry: dict) -> str | None:
        # All feeds are politics-focused; keep a consistent category label.
        return "All"
