"""Application configuration."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    app_name: str
    default_currency: str


def load_config() -> AppConfig:
    return AppConfig(
        app_name=os.getenv("APP_NAME", "learning-service"),
        default_currency=os.getenv("DEFAULT_CURRENCY", "USD"),
    )
