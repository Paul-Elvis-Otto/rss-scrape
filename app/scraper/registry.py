from __future__ import annotations

from .sites.bbc import BBCScraper
from .sites.dw import DWScraper
from .sites.spiegel import SpiegelPoliticsScraper
from .sites.bild import BILDScraper


def get_scrapers():
    # Add new site scrapers here
    return [
        BBCScraper(),
        DWScraper(),
        SpiegelPoliticsScraper(),
        BILDScraper(),
    ]
