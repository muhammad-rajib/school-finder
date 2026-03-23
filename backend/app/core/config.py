from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    DEBUG: bool
    RUN_ENV: str = "local"
    BASE_URL: str

    DATABASE_URL: str
    DOCKER_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str

    ALLOWED_ORIGINS: str

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "on", "debug", "development"}:
                return True
            if normalized in {"false", "0", "no", "off", "release", "production"}:
                return False
        return value

    @field_validator("RUN_ENV", mode="before")
    @classmethod
    def parse_run_env(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"docker", "local"}:
                return normalized
        return "local" if value is None else value

    @property
    def effective_database_url(self) -> str:
        if self.RUN_ENV == "docker":
            return self.DOCKER_DATABASE_URL
        return self.DATABASE_URL

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def masked_database_url(self) -> str:
        parts = urlsplit(self.effective_database_url)

        if "@" not in parts.netloc:
            return self.effective_database_url

        credentials, host = parts.netloc.rsplit("@", 1)
        username = credentials.split(":", 1)[0]
        masked_netloc = f"{username}:***@{host}"
        return urlunsplit((parts.scheme, masked_netloc, parts.path, parts.query, parts.fragment))


@lru_cache
def get_settings() -> Settings:
    return Settings()
