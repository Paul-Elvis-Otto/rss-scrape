import os


def env(name: str, default: str | None = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


DB_HOST = env("DB_HOST", "db")
DB_PORT = int(env("DB_PORT", "3306"))
DB_NAME = env("DB_NAME", "rss")
DB_USER = env("DB_USER", "rss")
DB_PASSWORD = env("DB_PASSWORD", "rss")

DB_ECHO = env("DB_ECHO", "false").lower() == "true"

SCRAPE_INTERVAL_SECONDS = int(env("SCRAPE_INTERVAL_SECONDS", "300"))

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)
