#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

"""
    Global Modules
"""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings, object):
    # SERVICE
    SERVICE_NAME: str = Field(default='Clear Read Hub Service', env='SERVICE_NAME')
    SERVICE_DESCRIPTION: str = Field(default='Clear Read Hub is a Platform for readability', env='SERVICE_DESCRIPTION')
    SERVICE_VERSION: str = Field(default='0.0.1', env='SERVICE_VERSION')
    # DB
    DB_SERVER_HOST: str = Field(default='', env='DB_SERVER_HOST')
    DB_USER: str = Field(default='', env='DB_USER')
    DB_PASSWORD: str = Field(default='', env='DB_PASSWORD')
    # Azure
    AZ_STORAGE_ACCOUNT_NAME: str = Field(default='devstoreaccount1', env='AZ_STORAGE_ACCOUNT_NAME')
    AZ_STORAGE_ACCOUNT_KEY: str = Field(
        default='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
        env='AZ_STORAGE_ACCOUNT_KEY'
    )
    AZ_STORAGE_BLOB_ENDPOINT: str = Field(default='http://127.0.0.1:10000/devstoreaccount1',
                                          env='AZ_STORAGE_BLOB_ENDPOINT')
    AZ_STORAGE_HTTPS: bool = Field(default=False, env='AZ_STORAGE_HTTPS')
    AZ_STORAGE_CONTAINER_NAME: str = Field(default='', env='AZ_STORAGE_CONTAINER_NAME')
    AZ_STORAGE_CONNECTION_STRING: str = ""
    # Sentry
    SENTRY_DSN: str = Field(default='', env='SENTRY_DSN')

    @field_validator('AZ_STORAGE_CONNECTION_STRING', check_fields=True)
    def generate_connection_string(cls, v, values):
        az_storage_https = values.data['AZ_STORAGE_HTTPS'] if 'AZ_STORAGE_HTTPS' in values.data else None
        az_storage_account_name = values.data['AZ_STORAGE_ACCOUNT_NAME'] if 'AZ_STORAGE_ACCOUNT_NAME' in values.data else None
        az_storage_account_key = values.data['AZ_STORAGE_ACCOUNT_KEY'] if 'AZ_STORAGE_ACCOUNT_KEY' in values.data else None
        az_storage_blob_endpoint = values.data['AZ_STORAGE_BLOB_ENDPOINT'] if 'AZ_STORAGE_BLOB_ENDPOINT' in values.data else None

        if all(item is not None for item in
               [az_storage_https, az_storage_account_name, az_storage_account_key, az_storage_blob_endpoint]):
            return (
                f"DefaultEndpointsProtocol={('https', 'http')[az_storage_https]};"
                f"AccountName={az_storage_account_name};"
                f"AccountKey={az_storage_account_key};"
                f"BlobEndpoint={az_storage_blob_endpoint};"
            )
    # CORS
    APP_CONSUMER_ORIGIN: str = Field(default='', env='APP_CONSUMER_ORIGIN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


coresettings = CoreSettings()
