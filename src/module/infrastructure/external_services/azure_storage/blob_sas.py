from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions


class AzureStorageBlobSas:
    def __init__(self, blob_client, account_key):
        self.blob_client = blob_client
        self.account_key = account_key

    def generate_read_sas(self):
        sas_token = generate_blob_sas(
            self.blob_client.account_name,
            self.blob_client.container_name,
            self.blob_client.blob_name,
            account_key=self.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # SAS token will be valid for 1 hour
        )
        return f"{self.blob_client.url}?{sas_token}"

    def generate_write_sas(self):
        sas_token = generate_blob_sas(
            account_name=self.blob_client.account_name,
            container_name=self.blob_client.container_name,
            blob_name=self.blob_client.blob_name,
            account_key=self.account_key,
            permission=BlobSasPermissions(write=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # SAS token will be valid for 1 hour
        )
        return f"{self.blob_client.url}?{sas_token}"

    def generate_non_expiry_sas(self):
        sas_token = generate_blob_sas(
            account_name=self.blob_client.account_name,
            container_name=self.blob_client.container_name,
            blob_name=self.blob_client.blob_name,
            account_key=self.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.max  # SAS token will never expire
        )
        return f"{self.blob_client.url}?{sas_token}"
