#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class StorageBackend(StrEnum):
    LOCAL = "local"
    AZURE = "azure"


class QueueBackend(StrEnum):
    # Process documents inside the API process, right after the upload.
    INLINE = "inline"
    # Hand documents to a Redis Queue (RQ) worker.
    RQ = "rq"


class ServiceConfig(BaseSettings):
    """
    Service configuration, read from environment variables and an optional `.env` file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # SERVICE
    SERVICE_NAME: str = "Clear Read Hub Service"
    SERVICE_DESCRIPTION: str = "Clear Read Hub is a Platform for readability"
    SERVICE_VERSION: str = "0.1.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    LOG_LEVEL: str = "INFO"

    # SECURITY
    JWT_SECRET_KEY: SecretStr = Field(min_length=32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = Field(default=15, gt=0)
    BCRYPT_ROUNDS: int = Field(default=12, ge=4, le=31)

    # CORS (comma separated list of origins)
    CORS_ALLOWED_ORIGINS: str = ""

    # MONGODB
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE_NAME: str = "clearreadhub"
    MONGODB_TIMEOUT_MS: int = Field(default=5000, gt=0)

    # STORAGE
    STORAGE_BACKEND: StorageBackend = StorageBackend.LOCAL
    LOCAL_STORAGE_PATH: str = "./data/uploads"
    AZ_STORAGE_CONNECTION_STRING: SecretStr | None = None
    AZ_STORAGE_CONTAINER_NAME: str = "documents"

    # DOCUMENTS
    MAX_UPLOAD_BYTES: int = Field(default=10 * 1024 * 1024, gt=0)
    MAX_PDF_PAGES: int = Field(default=500, gt=0)

    # QUEUE
    QUEUE_BACKEND: QueueBackend = QueueBackend.INLINE
    REDIS_URL: str = "redis://localhost:6379/0"
    QUEUE_NAME: str = "documents"
    JOB_TIMEOUT_SECONDS: int = Field(default=300, gt=0)
    JOB_MAX_RETRIES: int = Field(default=3, ge=0)

    # SENTRY
    SENTRY_DSN: str = ""
    SENTRY_TRACES_SAMPLE_RATE: float = Field(default=0.1, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def check_storage_backend(self) -> "ServiceConfig":
        if (
            self.STORAGE_BACKEND == StorageBackend.AZURE
            and not self.AZ_STORAGE_CONNECTION_STRING
        ):
            raise ValueError(
                "AZ_STORAGE_CONNECTION_STRING is required when STORAGE_BACKEND=azure"
            )
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> ServiceConfig:
    """
    Load the service configuration once per process.
    """
    return ServiceConfig()
