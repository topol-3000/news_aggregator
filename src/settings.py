from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve()


class AccessTokenSettings(BaseModel):
    lifetime_seconds: int = Field(
        default=3600, ge=300, le=86400
    )  # must be 5 min - 24 hours
    reset_password_token_secret: str
    verification_token_secret: str


class APISettings(BaseModel):
    title: str = "Octopus"
    description: str = "API for News Aggregator with AI Summarization"
    version: str = "0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    cors_origins: list[str] = ["*"]


class DatabaseSettings(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)
    user: str
    password: str
    name: str
    debug: bool = False
    pool_size: int = Field(default=100, gt=0)
    max_overflow: int = Field(default=50, ge=0)

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class LoggerSettings(BaseModel):
    level: LogLevel = LogLevel.DEBUG


# class CelerySettings(BaseModel):
#     broker_url: AnyUrl
#     backend_url: AnyUrl


class Settings(BaseSettings):
    access_token: AccessTokenSettings
    api: APISettings = APISettings()
    db: DatabaseSettings
    logger: LoggerSettings = LoggerSettings()
    # celery: CelerySettings

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env",),
        env_nested_delimiter="__",
        env_prefix="",
        case_sensitive=False,
    )


try:
    settings = Settings()
except Exception as e:
    import sys

    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)
