from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, BlobClient

from src.service_config import serviceConfig


class AzureStorageBlobSas:
    def __init__(self, blob_client: BlobClient):
        self.blob_client = blob_client

    def generate_read_sas(self):
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

    def generate_write_sas(self):
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

    def generate_non_expiry_sas(self):
        sas_token = generate_blob_sas(
            account_name=self.blob_client.account_name,
            container_name=self.blob_client.container_name,
            blob_name=self.blob_client.blob_name,
            account_key=serviceConfig.AZ_STORAGE_ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.max,  # SAS token will never expire
        )
        return f"{self.blob_client.url}?{sas_token}"
