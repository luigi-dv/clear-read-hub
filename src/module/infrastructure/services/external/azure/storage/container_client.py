#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
    Global Modules
"""
import sentry_sdk
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

"""
    Infrastructure Modules
"""
from src.module.infrastructure.logging.services.external.azure.logging import (
    AzureLogging,
)
from src.service_config import serviceConfig


class AzureStorageContainerClient:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            serviceConfig.AZ_STORAGE_CONNECTION_STRING
        )
        self.client = self.__create_container_client()

    def delete_container(self):
        """
        Deletes the container client under the main application container
        """
        container_client = self.blob_service_client.get_container_client(
            serviceConfig.AZ_STORAGE_CONTAINER_NAME
        )
        try:
            container_client.delete_container()
            return True
        except ResourceNotFoundError as e:
            # Capture Resource Not Found
            logging = AzureLogging("Storage", "Container Client", "Not Found")
            with sentry_sdk.push_scope() as scope:
                logging.set_sentry_tag(scope)
                logging.set_sentry_extra(scope)
                sentry_sdk.capture_exception(e)

    def __create_container_client(self):
        """
        Creates a container client under the main application container
        if the container with the specified name does not exist.
        """
        container_client = self.blob_service_client.get_container_client(
            serviceConfig.AZ_STORAGE_CONTAINER_NAME
        )
        try:
            # Try to get the container properties
            container_client.get_container_properties()
        except ResourceNotFoundError as e:
            # Capture Resource Not Found
            logging = AzureLogging("Storage", "Container Client", "Not Found")
            with sentry_sdk.push_scope() as scope:
                logging.set_sentry_tag(scope)
                logging.set_sentry_extra(scope)
                sentry_sdk.capture_exception(e)
            # If the container does not exist, create it
            container_client.create_container()

        # Return the container client
        return container_client
