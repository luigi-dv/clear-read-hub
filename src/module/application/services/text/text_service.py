import fitz

from src.module.domain.entities.files.data.file_data_extracted import FileDataExtracted

"""
    Infrastructure Modules
"""
from src.module.infrastructure.services.external.azure.storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.configuration.files_loader import load_responses

"""
    Domain Modules
"""
from src.module.domain.entities.files.data.file_data import FileData
from src.module.domain.services.external.azure.storage.file_reader import (
    AzureStorageFileReader,
)


class TextService:
    """
    Proxy Class for Text Service
    """

    def __init__(self, file_name: str):
        self.fn = file_name
        self.responses = load_responses()

    @property
    def file_name(self) -> str:
        """
        File name property
        Returns:
            - str: file name
        """
        return self.fn

    def __f_read(self) -> FileData:
        """
        Reads the file from the Azure Storage Linked Account

        Returns:
        - list[io.BytesIO]: A list of BytesIO objects containing the file content.
        """
        # Get the container client
        container_client = AzureStorageContainerClient().client
        # Get the blob client
        blob_client = container_client.get_blob_client(self.fn)
        file_reader = AzureStorageFileReader(blob_client)
        file_data = file_reader.read_file_data()
        return file_data

    def extract_text_from_pdf(self) -> FileDataExtracted:
        """
        The following method converts a pdf file to text

        Returns:
            - list[str]: A list of text strings, each string representing the text content of a page.
        """
        text_list = []
        file_data = self.__f_read()

        for data in file_data.data:
            doc = fitz.open(stream=data, filetype="pdf")
            page_texts = [page.get_text("text") for page in doc.pages()]
            text = "\n".join(page_texts)
            text_list.append(text)

        file_data_extracted = FileDataExtracted(file_data, text_list)
        return file_data_extracted
