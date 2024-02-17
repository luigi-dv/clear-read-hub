from azure.storage.blob import BlobClient

from src.service_config import serviceConfig
from src.module.domain.entities.file import File
from src.module.domain.repositories.file_repository import FileRepository
from src.module.infrastructure.external_services.azure_storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.external_services.azure_storage.file_uploader import (
    AzureStorageFileUploader,
)
from src.module.infrastructure.external_services.azure_storage.blob_sas import (
    AzureStorageBlobSas,
)


class AzureStorageFileInterface(FileRepository):
    def __init__(self):
        pass

    async def save(self, file: File) -> BlobClient:
        uploader = AzureStorageFileUploader(serviceConfig.AZ_STORAGE_CONNECTION_STRING)
        container_client = AzureStorageContainerClient().client
        # Upload the file
        blob_client = uploader.upload_file(
            file.content.read(), container_client.container_name, file.filename
        )
        # Return the blob client
        return blob_client

    async def get_sas_token_url(self, blob_client: BlobClient) -> str:
        # Create a new instance of the AzureStorageBlobSas class
        azure_blob_sas = AzureStorageBlobSas(blob_client)

        # Return the blob URL with the SAS token
        return azure_blob_sas.generate_read_sas()
