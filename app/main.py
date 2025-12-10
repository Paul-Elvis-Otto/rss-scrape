from __future__ import annotations

import time

from sqlalchemy.dialects.mysql import insert

from .config import SCRAPE_INTERVAL_SECONDS
from .db import SessionLocal, init_db
from .models import Article
from .scraper.registry import get_scrapers


def upsert_articles(session, articles):
    if not articles:
        return 0

    values = [
        dict(
            title=a.title,
            url=a.url,
            published_at=a.published_at,
            category=a.category,
            platform=a.platform,
        )
        for a in articles
    ]

    stmt = insert(Article).values(values)

    # If URL already exists, update metadata.
    update_dict = {
        "title": stmt.inserted.title,
        "published_at": stmt.inserted.published_at,
        "category": stmt.inserted.category,
        "platform": stmt.inserted.platform,
    }

    stmt = stmt.on_duplicate_key_update(**update_dict)
    result = session.execute(stmt)
    return result.rowcount or 0


def run_once():
    scrapers = get_scrapers()
    all_items = []

    try:
        for scraper in scrapers:
            try:
                scraped = scraper.scrape()
            except Exception as exc:
                # Log scraper-specific errors and continue with other scrapers.
                print(f"Error scraping {getattr(scraper, 'platform', scraper.__class__.__name__)}: {exc}")
                continue

            all_items.extend(scraped)
    finally:
        for scraper in scrapers:
            scraper.close()

    with SessionLocal() as session:
        count = upsert_articles(session, all_items)
        session.commit()

    print(f"Scraped {len(all_items)} items, upserted {count} rows.")


def main():
    init_db()

    while True:
        try:
            run_once()
        except Exception as exc:
            # Keep the service alive; log for debugging
            print(f"Error during scrape: {exc}")

        time.sleep(SCRAPE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
