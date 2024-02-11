#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'


"""
 Global Modules
"""
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError


class AzureStorageContainerClient:
    def __init__(self, connection_string, container_name):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name
        self.container_client = self.__create_container_client()

    def delete_container(self):
        # Delete the container
        container_client = self.blob_service_client.get_container_client(self.container_name)
        container_client.delete_container()

        return True

    def __create_container_client(self):
        # Create a new container client
        container_client = self.blob_service_client.get_container_client(self.container_name)
        try:
            # Try to get the container properties
            container_client.get_container_properties()
        except ResourceNotFoundError:
            # If the container does not exist, create it
            container_client.create_container()
        # Return the container client
        return container_client
