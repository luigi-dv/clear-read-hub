#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class ServiceConfig(BaseSettings, object):
    # SERVICE
    SERVICE_NAME: str = Field(default="Clear Read Hub Service", env="SERVICE_NAME")
    SERVICE_DESCRIPTION: str = Field(
        default="Clear Read Hub is a Platform for readability",
        env="SERVICE_DESCRIPTION",
    )
    SERVICE_VERSION: str = Field(default="0.0.1", env="SERVICE_VERSION")
    # OAuth
    SERVICE_OAUTH_CLIENT_ID: str = Field(default="", env="SERVICE_OAUTH_CLIENT_ID")
    SERVICE_OAUTH_CLIENT_SECRET: str = Field(
        default="", env="SERVICE_OAUTH_CLIENT_SECRET"
    )
    SERVICE_OAUTH_ENCODE_ALGORITHM: str = Field(
        default="HS256", env="SERVICE_OAUTH_ENCODE_ALGORITHM"
    )
    SERVICE_OAUTH_EXPIRES_IN: int = Field(default=15, env="SERVICE_OAUTH_EXPIRES_IN")
    # MONGODB
    MONGODB_INITDB_ROOT_HOST: str = Field(
        default="localhost", env="MONGODB_INITDB_ROOT_HOST"
    )
    MONGODB_INITDB_ROOT_PORT: int = Field(default=27017, env="MONGODB_INITDB_ROOT_PORT")
    MONGODB_INITDB_ROOT_USERNAME: str = Field(
        default="clearreadhub", env="MONGODB_INITDB_ROOT_USERNAME"
    )
    MONGODB_INITDB_ROOT_PASSWORD: str = Field(
        default="root", env="MONGODB_INITDB_ROOT_PASSWORD"
    )
    MONGODB_DATABASE_NAME: str = Field(
        default="clearreadhub", env="MONGODB_DATABASE_NAME"
    )
    MONGO_INITDB_CONNECTION_STRING: str = ""
    # Azure
    AZ_STORAGE_ACCOUNT_NAME: str = Field(
        default="devstoreaccount1", env="AZ_STORAGE_ACCOUNT_NAME"
    )
    AZ_STORAGE_ACCOUNT_KEY: str = Field(
        default="Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==",
        env="AZ_STORAGE_ACCOUNT_KEY",
    )
    AZ_STORAGE_BLOB_ENDPOINT: str = Field(
        default="http://127.0.0.1:10000/devstoreaccount1",
        env="AZ_STORAGE_BLOB_ENDPOINT",
    )
    AZ_STORAGE_HTTPS: bool = Field(default=False, env="AZ_STORAGE_HTTPS")
    AZ_STORAGE_CONTAINER_NAME: str = Field(default="", env="AZ_STORAGE_CONTAINER_NAME")
    AZ_STORAGE_CONNECTION_STRING: str = ""
    # Sentry
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    # CORS
    APP_CONSUMER_ORIGIN: str = Field(default="", env="APP_CONSUMER_ORIGIN")

    @field_validator("AZ_STORAGE_CONNECTION_STRING", check_fields=True)
    def generate_connection_string(cls, v, values):
        az_storage_https = (
            values.data["AZ_STORAGE_HTTPS"]
            if "AZ_STORAGE_HTTPS" in values.data
            else None
        )
        az_storage_account_name = (
            values.data["AZ_STORAGE_ACCOUNT_NAME"]
            if "AZ_STORAGE_ACCOUNT_NAME" in values.data
            else None
        )
        az_storage_account_key = (
            values.data["AZ_STORAGE_ACCOUNT_KEY"]
            if "AZ_STORAGE_ACCOUNT_KEY" in values.data
            else None
        )
        az_storage_blob_endpoint = (
            values.data["AZ_STORAGE_BLOB_ENDPOINT"]
            if "AZ_STORAGE_BLOB_ENDPOINT" in values.data
            else None
        )

        if all(
            item is not None
            for item in [
                az_storage_https,
                az_storage_account_name,
                az_storage_account_key,
                az_storage_blob_endpoint,
            ]
        ):
            return (
                f"DefaultEndpointsProtocol={('https', 'http')[az_storage_https]};"
                f"AccountName={az_storage_account_name};"
                f"AccountKey={az_storage_account_key};"
                f"BlobEndpoint={az_storage_blob_endpoint};"
            )

    @field_validator("MONGO_INITDB_CONNECTION_STRING", check_fields=True)
    def generate_mongo_connection_string(cls, v, values):
        mongodb_init_db_root_host = (
            values.data["MONGODB_INITDB_ROOT_HOST"]
            if "MONGODB_INITDB_ROOT_HOST" in values.data
            else None
        )
        mongodb_init_db_root_port = (
            values.data["MONGODB_INITDB_ROOT_PORT"]
            if "MONGODB_INITDB_ROOT_PORT" in values.data
            else None
        )
        mongodb_init_db_root_username = (
            values.data["MONGODB_INITDB_ROOT_USERNAME"]
            if "MONGODB_INITDB_ROOT_USERNAME" in values.data
            else None
        )
        mongodb_init_db_root_password = (
            values.data["MONGODB_INITDB_ROOT_PASSWORD"]
            if "MONGODB_INITDB_ROOT_PASSWORD" in values.data
            else None
        )

        if all(
            item is not None
            for item in [mongodb_init_db_root_username, mongodb_init_db_root_password]
        ):
            return f"mongodb://{mongodb_init_db_root_username}:{mongodb_init_db_root_password}@{mongodb_init_db_root_host}:{mongodb_init_db_root_port}/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


serviceConfig = ServiceConfig()
