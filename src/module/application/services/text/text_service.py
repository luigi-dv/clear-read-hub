#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import fitz
from src.module.domain.entities.files.data.file_data_extracted import FileDataExtracted
from src.module.infrastructure.machine_learning.bert_model import BertModel
from src.module.infrastructure.services.external.azure.storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.configuration.files_loader import load_responses
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
        :return: The file name
        """
        return self.fn

    def __f_read(self) -> FileData:
        """
        Reads the file from the Azure Storage Linked Account

        :return: A list of BytesIO objects containing the file content.
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
        Extracts text from a pdf file

        :return: A list of text strings, each string representing the text content of a page.
        """
        data_list = []
        file_data = self.__f_read()

        for data in file_data.data:
            doc = fitz.open(stream=data, filetype="pdf")
            for i, page in enumerate(doc):
                text = page.get_text("text")
                # Append the text of each page to the list
                data_list.append(text)

        file_data_extracted = FileDataExtracted(file_data, data_list)
        return file_data_extracted

    def process_text(self):
        """
        Processes the text

        :return: The processed text
        """

        file_data_extracted = self.extract_text_from_pdf()
        classifier_model = BertModel(file_data_extracted.extracted_text)
        return classifier_model.bert_raw_result
