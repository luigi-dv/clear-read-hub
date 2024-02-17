#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
    Service Configuration
"""
from src.service_config import serviceConfig

"""
    Infrastructure Modules
"""
from src.module.infrastructure.message_queue.task_queue import get_task_queue
from src.module.infrastructure.external_services.azure_storage.file_uploader import (
    AzureStorageFileUploader,
)


# Initialize AzureStorageFileUploader
azure_uploader = AzureStorageFileUploader(serviceConfig.AZ_STORAGE_CONNECTION_STRING)


def azure_upload_worker():
    q = get_task_queue()
    while True:
        job = q.dequeue()
        if job is not None and job.func_name == "upload_file":
            file_content, container_name, blob_name = job.args
            # Use AzureStorageFileUploader to upload the file
            azure_uploader.upload_file(file_content, container_name, blob_name)
