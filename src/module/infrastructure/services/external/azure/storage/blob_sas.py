from datetime import datetime, timedelta

import sentry_sdk
from azure.common import AzureException
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, BlobClient

from src.service_config import serviceConfig

"""
    Infrastructure Modules
"""
from src.module.infrastructure.logging.services.external.azure.logging import (
    AzureLogging,
)


class AzureStorageBlobSas:
    def __init__(self, blob_client: BlobClient):
        self.blob_client = blob_client

    def generate_read_sas(self):
        """
        Generates a SAS Token with read permissions under the specific Blob
        """
        try:
            sas_token = generate_blob_sas(
                self.blob_client.account_name,
                self.blob_client.container_name,
                self.blob_client.blob_name,
                account_key=serviceConfig.AZ_STORAGE_ACCOUNT_KEY,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow()
                + timedelta(hours=1),  # SAS token will be valid for 1 hour
            )
            return f"{self.blob_client.url}?{sas_token}"
        except AzureException as e:
            logging = AzureLogging("Storage", "SAS", "Read Token")
            with sentry_sdk.push_scope() as scope:
                logging.set_sentry_tag(scope)
                logging.set_sentry_extra(scope)
                sentry_sdk.capture_exception(e)

    def generate_write_sas(self):
        """
        Generates a SAS Token with write permissions under the specific Blob.
        """
        try:
            sas_token = generate_blob_sas(
                account_name=self.blob_client.account_name,
                container_name=self.blob_client.container_name,
                blob_name=self.blob_client.blob_name,
                account_key=serviceConfig.AZ_STORAGE_ACCOUNT_KEY,
                permission=BlobSasPermissions(write=True),
                expiry=datetime.utcnow()
                + timedelta(hours=1),  # SAS token will be valid for 1 hour
            )
            return f"{self.blob_client.url}?{sas_token}"
        except AzureException as e:
            logging = AzureLogging("Storage", "SAS", "Write Token")
            with sentry_sdk.push_scope() as scope:
                logging.set_sentry_tag(scope)
                logging.set_sentry_extra(scope)
                sentry_sdk.capture_exception(e)

    def generate_non_expiry_sas(self):
        """
        Generates a non Expire SAS Token with Read permissions under the specific Blob.
        """
        try:
            sas_token = generate_blob_sas(
                account_name=self.blob_client.account_name,
                container_name=self.blob_client.container_name,
                blob_name=self.blob_client.blob_name,
                account_key=serviceConfig.AZ_STORAGE_ACCOUNT_KEY,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.max,  # SAS token will never expire
            )
            return f"{self.blob_client.url}?{sas_token}"
        except AzureException as e:
            logging = AzureLogging("Storage", "SAS", "Non-expiry Read Token")
            with sentry_sdk.push_scope() as scope:
                logging.set_sentry_tag(scope)
                logging.set_sentry_extra(scope)
                sentry_sdk.capture_exception(e)
