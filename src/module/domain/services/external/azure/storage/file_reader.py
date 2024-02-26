"""
    Global Modules
"""

import io
from azure.storage.blob import BlobClient
from fastapi import HTTPException

from src.module.infrastructure.configuration.files_loader import load_responses

"""
    Domain Modules
"""
from src.module.domain.entities.files.data.file_data import FileData


class AzureStorageFileReader:
    """
    Domain service for reading file data from Azure Storage.

    Attributes:
        - `blob_client` (BlobClient): The Azure Storage BlobClient used to interact with the blob.
    """

    def __init__(self, blob_client: BlobClient):
        """
        Initialize the AzureStorageFileReader.

        Parameters:
            - `blob_client` (BlobClient): The Azure Storage BlobClient used to interact with the blob.
        """
        self.blob_client = blob_client
        self.responses = load_responses()

    def read_file_data(self) -> FileData:
        """
        Read the file data from Azure Storage.

        Returns:
            - FileData: An entity containing the file content.

        Raises:
            - HTTPException: If the file is not found.
        """
        if self.blob_client.exists():
            # Get File Data
            blob_data = [io.BytesIO(self.blob_client.download_blob().readall())]
            # Get File Properties
            blob_properties = self.blob_client.get_blob_properties()
            return FileData(
                name=blob_properties.name,
                data=blob_data,
                metadata=blob_properties.metadata,
                file_type=blob_properties.blob_type,
                size=blob_properties.size,
                creation_time=blob_properties.creation_time,
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=self.responses.module.domain.services.external.error.not_found,
            )
