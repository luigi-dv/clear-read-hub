#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

"""
    Global Modules
"""
from pydantic import Field
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
    AZ_STORAGE_ACCOUNT_NAME: str = Field(default='', env='AZ_STORAGE_ACCOUNT_NAME')
    AZ_STORAGE_ACCOUNT_KEY: str = Field(default='', env='AZ_STORAGE_ACCOUNT_KEY')
    AZ_STORAGE_CONNECTION_STRING: str = Field(default='', env='AZ_STORAGE_CONNECTION_STRING')
    AZ_STORAGE_CONTAINER_NAME: str = Field(default='', env='AZ_STORAGE_CONTAINER_NAME')
    # CORS
    APP_CONSUMER_ORIGIN: str = Field(default='', env='APP_CONSUMER_ORIGIN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


coresettings = CoreSettings()
