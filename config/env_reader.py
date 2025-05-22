from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import RedisDsn, field_validator
from pydantic_settings import BaseSettings

env_file = Path(__file__).resolve().parent.parent / ".env"

if env_file.exists():
    load_dotenv(dotenv_path=env_file)


class VariablesFromEnvironment(BaseSettings):
    """Defines environment variables with their types"""

    SECRET_KEY: Optional[str] = (
        "django-insecure-@m5^ry7)zhwwo*8z%tqahkfo@r!_vg=sc!_&u4ki1e-g)p#x_9"
    )

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    CACHE_DB: Optional[RedisDsn] = "redis://localhost:6379/0"
    DRAMATIQ_BROKER_URL: Optional[RedisDsn] = "redis://localhost:6379"
    DRAMATIQ_RESULTS_URL: Optional[RedisDsn] = "redis://localhost:6379"

    CSRF_TRUSTED_ORIGINS: Optional[str] = (
        # Website, frontend urls separated with comma
        "http://localhost:8000"
    )

    # hosts domains separated with comma
    ALLOWED_HOSTS: str = "127.0.0.1,localhost"

    ENVIRONMENT: str = "production"

    # AWS S3 settings
    AWS_ACCESS_KEY_ID: Optional[str] = ""
    AWS_S3_CUSTOM_DOMAIN: Optional[str] = ""
    AWS_SECRET_ACCESS_KEY: Optional[str] = ""
    AWS_STORAGE_BUCKET_NAME: Optional[str] = ""
    AWS_PRESIGNED_EXPIRY: int = 100
    AWS_S3_REGION_NAME: Optional[str] = ""
    AWS_S3_ORIGIN_URL: Optional[str] = ""
    AWS_S3_ROOT_URL: Optional[str] = ""

    # Sentry settings
    SENTRY_DSN: Optional[str] = ""
    SENTRY_SAMPLE_RATE: int = 0
    SENTRY_ENABLE_TRACING: bool = True

    class Config:
        """Defines configuration for pydantic environment loading"""

        case_sensitive = True
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._process_fields()

    @field_validator("ENVIRONMENT")
    def validate_environment(cls, value):
        if value not in {"development", "production"}:
            raise ValueError("ENVIRONMENT must be either 'development' or 'production'")
        return value

    @field_validator("CSRF_TRUSTED_ORIGINS")
    def validate_csrf_trusted_origins(cls, value):
        if isinstance(value, str):
            urls = [url.strip() for url in value.split(",")]
            for url in urls:
                if not url.startswith("http"):
                    raise ValueError(f"Invalid URL: {url}")
            return urls
        raise ValueError(
            "CSRF_TRUSTED_ORIGINS must be a comma-separated string of URLs"
        )

    @field_validator("ALLOWED_HOSTS")
    def validate_allowed_hosts(cls, value):
        if isinstance(value, str):
            urls = [url.strip() for url in value.split(",")]
            return urls
        raise ValueError("ALLOWED_HOSTS must be a comma-separated string of domains")

    def _process_fields(self):
        for name, value in self.__dict__.items():
            if isinstance(value, str):
                setattr(self, name, value.strip())
            elif isinstance(value, list) and all(isinstance(v, str) for v in value):
                setattr(self, name, [v.strip() for v in value if v.strip()])


env = VariablesFromEnvironment()
