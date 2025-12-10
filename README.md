# RSS scraper

Simple RSS/Atom scraper that writes items to MariaDB with per-site scraper modules.

## Quick start
- Ensure Docker and Docker Compose are installed.
- Adjust `.env` if needed (DB credentials, host, optional `DB_ECHO`).
- Build and run: `docker compose up --build`.
- Logs from the scraper container will show scrape counts every interval (default 600s).

## Adding a site
- Add a file under `app/scraper/sites/` that subclasses `BaseScraper` and defines `platform`, `feeds`, and `infer_category`.
- Register it in `app/scraper/registry.py`.
