"""Application configuration loaded from environment / .env file."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "ExhibitionHunter API"
    debug: bool = False
    api_v1_prefix: str = "/api"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/exhibitions.db"

    # Crawler
    crawler_default_engine: str = "auto"  # auto | httpx | playwright
    crawler_max_concurrency: int = 4
    crawler_user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )
    # Only crawl exhibitions starting within the next N months (plus ongoing)
    crawler_future_months: int = 3

    # Scheduler
    scheduler_enabled: bool = False
    scheduler_crawl_cron: str = "0 3 * * *"

    # Logging
    log_level: str = "INFO"
    log_dir: str = "./data/logs"

    @property
    def db_path(self) -> Path:
        """Resolve sqlite file path under backend root."""
        url = self.database_url
        if url.startswith("sqlite"):
            # strip scheme prefix "sqlite:///./" or "sqlite+aiosqlite:///./"
            for prefix in ("sqlite+aiosqlite:///", "sqlite:///"):
                if url.startswith(prefix):
                    rel = url[len(prefix):]
                    return (BACKEND_ROOT / rel).resolve()
        return BACKEND_ROOT / "data" / "exhibitions.db"


settings = Settings()

# Ensure data dirs exist
(BACKEND_ROOT / "data").mkdir(parents=True, exist_ok=True)
(BACKEND_ROOT / settings.log_dir).mkdir(parents=True, exist_ok=True)
