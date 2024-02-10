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
    # CORS
    APP_CONSUMER_ORIGIN: str = Field(default='', env='APP_CONSUMER_ORIGIN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


coresettings = CoreSettings()
